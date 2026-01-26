# -*- coding: utf-8 -*-

from odoo import fields, models


class EduTeacher(models.Model):
    _name = "edu.teacher"
    _description = "Teacher"
    _order = "name"

    name = fields.Char(required=True, index=True)
    employee_code = fields.Char(index=True, copy=False)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    subject_ids = fields.Many2many(
        "edu.academic.subject",
        "edu_teacher_subject_rel",
        "teacher_id",
        "subject_id",
        string="Subjects",
    )
    class_ids = fields.Many2many(
        "edu.academic.class",
        "edu_teacher_class_rel",
        "teacher_id",
        "class_id",
        string="Classes",
    )
