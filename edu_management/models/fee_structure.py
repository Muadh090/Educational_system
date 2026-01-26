# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FeeStructure(models.Model):
    _name = "edu.fee.structure"
    _description = "Fee Structure"
    _order = "academic_year_id desc, name"

    name = fields.Char(required=True, index=True)
    academic_year_id = fields.Many2one(
        "edu.academic.year",
        ondelete="restrict",
        index=True,
    )
    term_id = fields.Many2one(
        "edu.academic.term",
        string="Term",
        ondelete="restrict",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        ondelete="restrict",
        index=True,
    )
    line_ids = fields.One2many(
        "edu.fee.line",
        "fee_structure_id",
        string="Fee Lines",
    )
    total_amount = fields.Monetary(
        compute="_compute_total_amount",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    _sql_constraints = [
        (
            "fee_structure_unique",
            "unique(academic_year_id, term_id, class_id, company_id)",
            "Only one fee structure per year/term/class is allowed.",
        )
    ]

    @api.depends("line_ids.subtotal")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped("subtotal"))

    @api.constrains("term_id", "academic_year_id")
    def _check_term_year(self):
        for record in self:
            if record.term_id and record.academic_year_id:
                if record.term_id.academic_year_id != record.academic_year_id:
                    raise ValidationError("Term must belong to the selected academic year.")
