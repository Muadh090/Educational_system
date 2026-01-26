# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AcademicClass(models.Model):
    _name = "edu.academic.class"
    _description = "Academic Class"
    _order = "name"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True, copy=False)
    academic_year_id = fields.Many2one(
        "edu.academic.year",
        required=False,
        ondelete="restrict",
        index=True,
    )
    term_id = fields.Many2one(
        "edu.academic.term",
        ondelete="restrict",
        index=True,
    )
    section_ids = fields.One2many(
        "edu.academic.section",
        "class_id",
        string="Sections",
    )
    subject_ids = fields.Many2many(
        "edu.academic.subject",
        "edu_class_subject_rel",
        "class_id",
        "subject_id",
        string="Subjects",
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
            "class_code_company_uniq",
            "unique(code, company_id)",
            "The class code must be unique per company.",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code"):
                vals["code"] = self.env["ir.sequence"].next_by_code("edu.academic.class")
        return super().create(vals_list)
