# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FeeLine(models.Model):
    _name = "edu.fee.line"
    _description = "Fee Line"
    _order = "sequence, id"

    fee_structure_id = fields.Many2one(
        "edu.fee.structure",
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
    product_id = fields.Many2one(
        "product.product",
        required=True,
        domain="[(\"sale_ok\", \"=\", True)]",
    )
    quantity = fields.Float(default=1.0)
    price_unit = fields.Monetary(required=True)
    subtotal = fields.Monetary(compute="_compute_subtotal", store=True)
    currency_id = fields.Many2one(
        "res.currency",
        related="fee_structure_id.currency_id",
        store=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="fee_structure_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = (record.quantity or 0.0) * (record.price_unit or 0.0)

    @api.constrains("quantity", "price_unit")
    def _check_amounts(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")
            if record.price_unit < 0:
                raise ValidationError("Unit price cannot be negative.")
