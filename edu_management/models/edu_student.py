# -*- coding: utf-8 -*-

from odoo import fields, models


class EduStudent(models.Model):
    _name = "edu.student"
    _description = "Student"
    _order = "name"

    name = fields.Char(required=True, index=True)
    student_code = fields.Char(index=True, copy=False)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        ondelete="restrict",
        index=True,
    )
    section_id = fields.Many2one(
        "edu.academic.section",
        string="Section",
        ondelete="restrict",
        index=True,
    )

    parent_ids = fields.Many2many(
        "edu.parent",
        "edu_student_parent_rel",
        "student_id",
        "parent_id",
        string="Parents / Guardians",
    )
