# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HostelManagement(models.Model):
    _name = "edu.hostel"
    _description = "Hostel Management"
    _order = "name"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True)
    capacity = fields.Integer(default=0)
    fee_structure_id = fields.Many2one(
        "edu.fee.structure",
        string="Fee Structure",
        ondelete="restrict",
        index=True,
    )
    student_ids = fields.Many2many(
        "edu.student",
        "edu_hostel_student_rel",
        "hostel_id",
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
            "hostel_name_company_uniq",
            "unique(name, company_id)",
            "The hostel name must be unique per company.",
        )
    ]

    @api.constrains("capacity", "student_ids")
    def _check_capacity(self):
        for record in self:
            if record.capacity and len(record.student_ids) > record.capacity:
                raise ValidationError("Allocated students exceed hostel capacity.")
