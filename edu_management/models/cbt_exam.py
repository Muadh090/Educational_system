# -*- coding: utf-8 -*-

from odoo import fields, models


class CBTExam(models.Model):
    _name = "edu.cbt.exam"
    _description = "CBT / Online Exam"
    _order = "start_datetime desc, id desc"

    name = fields.Char(required=True, index=True)
    instructions = fields.Html()
    start_datetime = fields.Datetime(required=True, index=True)
    end_datetime = fields.Datetime(required=True, index=True)
    duration_minutes = fields.Integer()

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
        "edu_cbt_exam_student_rel",
        "exam_id",
        "student_id",
        string="Eligible Students",
    )

    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )
