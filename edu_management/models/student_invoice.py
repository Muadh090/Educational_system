# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class StudentInvoice(models.Model):
    _name = "edu.student.invoice"
    _description = "Student Invoice"
    _order = "date desc, id desc"

    name = fields.Char(required=True, index=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    student_id = fields.Many2one(
        "edu.student",
        required=True,
        ondelete="restrict",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        ondelete="restrict",
        index=True,
    )
    term_id = fields.Many2one(
        "edu.academic.term",
        string="Term",
        ondelete="restrict",
        index=True,
    )
    fee_structure_id = fields.Many2one(
        "edu.fee.structure",
        ondelete="restrict",
        index=True,
    )

    line_ids = fields.One2many(
        "edu.student.invoice.line",
        "invoice_id",
        string="Invoice Lines",
    )
    amount_total = fields.Monetary(compute="_compute_amount_total", store=True)
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )

    move_id = fields.Many2one(
        "account.move",
        string="Accounting Invoice",
        readonly=True,
        ondelete="set null",
        index=True,
    )
    payment_status = fields.Selection(
        [
            ("unpaid", "Unpaid"),
            ("partial", "Partially Paid"),
            ("paid", "Paid"),
        ],
        compute="_compute_payment_status",
        store=True,
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    _sql_constraints = [
        (
            "student_invoice_unique",
            "unique(student_id, term_id, class_id, fee_structure_id)",
            "An invoice already exists for this student and fee structure context.",
        )
    ]

    @api.depends("line_ids.subtotal")
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.line_ids.mapped("subtotal"))

    @api.depends("move_id.payment_state")
    def _compute_payment_status(self):
        for record in self:
            state = record.move_id.payment_state if record.move_id else "not_paid"
            if state in ("paid", "in_payment"):
                record.payment_status = "paid"
            elif state in ("partial",):
                record.payment_status = "partial"
            else:
                record.payment_status = "unpaid"

    @api.onchange("fee_structure_id")
    def _onchange_fee_structure_id(self):
        if not self.fee_structure_id:
            self.line_ids = [(5, 0, 0)]
            return
        self.line_ids = [(5, 0, 0)]
        self.line_ids = [
            (0, 0, {
                "name": line.name,
                "fee_type": line.fee_type,
                "product_id": line.product_id.id,
                "quantity": line.quantity,
                "price_unit": line.price_unit,
            })
            for line in self.fee_structure_id.line_ids
        ]

    def action_generate_invoice(self):
        for record in self:
            if record.move_id:
                raise UserError("An accounting invoice is already linked.")
            if not record.line_ids:
                raise UserError("Please add fee lines before generating the invoice.")
            if not record.student_id:
                raise UserError("Please select a student.")

            partner = record.student_id.company_id.partner_id
            if record.student_id and hasattr(record.student_id, "partner_id") and record.student_id.partner_id:
                partner = record.student_id.partner_id

            invoice_lines = []
            for line in record.line_ids:
                if not line.product_id:
                    raise ValidationError("Each fee line must have a product.")
                account = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
                if not account:
                    raise ValidationError("Please set an income account on the product or its category.")
                invoice_lines.append(
                    (0, 0, {
                        "name": line.name,
                        "product_id": line.product_id.id,
                        "quantity": line.quantity,
                        "price_unit": line.price_unit,
                        "account_id": account.id,
                    })
                )

            move = self.env["account.move"].create({
                "move_type": "out_invoice",
                "invoice_date": record.date,
                "partner_id": partner.id,
                "invoice_line_ids": invoice_lines,
                "ref": record.name,
            })
            record.move_id = move.id


class StudentInvoiceLine(models.Model):
    _name = "edu.student.invoice.line"
    _description = "Student Invoice Line"
    _order = "sequence, id"

    invoice_id = fields.Many2one(
        "edu.student.invoice",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    fee_type = fields.Selection(
        [
            ("tuition", "Tuition"),
            ("textbook", "Textbook"),
            ("notebook", "Notebook"),
            ("optional", "Optional"),
        ],
        required=True,
        default="tuition",
    )
    product_id = fields.Many2one("product.product", required=True)
    quantity = fields.Float(default=1.0)
    price_unit = fields.Monetary(required=True)
    subtotal = fields.Monetary(compute="_compute_subtotal", store=True)
    currency_id = fields.Many2one(
        "res.currency",
        related="invoice_id.currency_id",
        store=True,
        readonly=True,
    )

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = (record.quantity or 0.0) * (record.price_unit or 0.0)
