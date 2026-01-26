# -*- coding: utf-8 -*-

from odoo import fields, models


class TransportManagement(models.Model):
    _name = "edu.transport"
    _description = "Transport Management"
    _order = "name"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True)
    route = fields.Char()
    fee_structure_id = fields.Many2one(
        "edu.fee.structure",
        string="Fee Structure",
        ondelete="restrict",
        index=True,
    )
    student_ids = fields.Many2many(
        "edu.student",
        "edu_transport_student_rel",
        "transport_id",
        "student_id",
        string="Allocated Students",
    )
    show_in_menu = fields.Boolean(default=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    _sql_constraints = [
        (
            "transport_name_company_uniq",
            "unique(name, company_id)",
            "The transport name must be unique per company.",
        )
    ]
