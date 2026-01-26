# -*- coding: utf-8 -*-

from odoo import fields, models


class Assignment(models.Model):
    _name = "edu.assignment"
    _description = "Assignment"
    _order = "due_date desc, id desc"

    name = fields.Char(required=True, index=True)
    description = fields.Html()
    due_date = fields.Datetime(index=True)

    teacher_id = fields.Many2one(
        "edu.teacher",
        required=True,
        ondelete="restrict",
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
    subject_id = fields.Many2one(
        "edu.academic.subject",
        string="Subject",
        ondelete="restrict",
        index=True,
    )

    student_ids = fields.Many2many(
        "edu.student",
        "edu_assignment_student_rel",
        "assignment_id",
        "student_id",
        string="Assigned Students",
    )

    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )
