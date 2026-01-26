# -*- coding: utf-8 -*-

from odoo import fields, models


class EduParent(models.Model):
    _name = "edu.parent"
    _description = "Parent / Guardian"
    _order = "name"

    name = fields.Char(required=True, index=True)
    phone = fields.Char()
    email = fields.Char()
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    student_ids = fields.Many2many(
        "edu.student",
        "edu_student_parent_rel",
        "parent_id",
        "student_id",
        string="Students",
    )
