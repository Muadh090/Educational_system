# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AcademicSection(models.Model):
    _name = "edu.academic.section"
    _description = "Academic Section"
    _order = "name"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True, copy=False)
    class_id = fields.Many2one(
        "edu.academic.class",
        required=True,
        ondelete="cascade",
        index=True,
    )
    capacity = fields.Integer(default=0)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        related="class_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _sql_constraints = [
        (
            "section_name_class_uniq",
            "unique(name, class_id)",
            "The section name must be unique per class.",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code"):
                vals["code"] = self.env["ir.sequence"].next_by_code("edu.academic.section")
        return super().create(vals_list)
