# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcademicYear(models.Model):
    _name = "edu.academic.year"
    _description = "Academic Year"
    _order = "date_start desc"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True)
    date_start = fields.Date(required=True, index=True)
    date_end = fields.Date(required=True, index=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )
    term_ids = fields.One2many(
        "edu.academic.term",
        "academic_year_id",
        string="Terms",
    )

    _sql_constraints = [
        (
            "year_name_company_uniq",
            "unique(name, company_id)",
            "The academic year name must be unique per company.",
        )
    ]

    @api.constrains("date_start", "date_end")
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("Start date must be earlier than end date.")
