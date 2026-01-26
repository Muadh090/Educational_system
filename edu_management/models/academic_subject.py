# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AcademicSubject(models.Model):
    _name = "edu.academic.subject"
    _description = "Academic Subject"
    _order = "name"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True, copy=False)
    class_ids = fields.Many2many(
        "edu.academic.class",
        "edu_class_subject_rel",
        "subject_id",
        "class_id",
        string="Classes",
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
            "subject_code_company_uniq",
            "unique(code, company_id)",
            "The subject code must be unique per company.",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code"):
                vals["code"] = self.env["ir.sequence"].next_by_code("edu.academic.subject")
        return super().create(vals_list)
