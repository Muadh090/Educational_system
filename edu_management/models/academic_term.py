# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcademicTerm(models.Model):
    _name = "edu.academic.term"
    _description = "Academic Term"
    _order = "date_start desc"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True)
    date_start = fields.Date(required=True, index=True)
    date_end = fields.Date(required=True, index=True)
    active = fields.Boolean(default=True)
    academic_year_id = fields.Many2one(
        "edu.academic.year",
        required=True,
        ondelete="restrict",
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="academic_year_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _sql_constraints = [
        (
            "term_name_year_uniq",
            "unique(name, academic_year_id)",
            "The term name must be unique per academic year.",
        )
    ]

    @api.constrains("date_start", "date_end", "academic_year_id")
    def _check_term_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("Start date must be earlier than end date.")
            if (
                record.academic_year_id
                and record.date_start
                and record.date_end
                and (
                    record.date_start < record.academic_year_id.date_start
                    or record.date_end > record.academic_year_id.date_end
                )
            ):
                raise ValidationError("Term dates must fall within the academic year.")
