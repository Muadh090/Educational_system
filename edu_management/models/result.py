# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Result(models.Model):
    _name = "edu.result"
    _description = "Result"
    _order = "date desc, id desc"

    name = fields.Char(required=True, index=True)
    date = fields.Date(required=True, index=True)
    result_type = fields.Selection(
        [
            ("class", "Class"),
            ("student", "Student"),
        ],
        required=True,
        default="class",
        index=True,
    )

    exam_id = fields.Many2one(
        "edu.exam",
        required=True,
        ondelete="restrict",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        required=True,
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
    student_id = fields.Many2one(
        "edu.student",
        string="Student",
        ondelete="restrict",
        index=True,
    )

    line_ids = fields.One2many(
        "edu.result.line",
        "result_id",
        string="Result Lines",
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    _sql_constraints = [
        (
            "result_exam_class_subject_unique",
            "unique(exam_id, class_id, section_id, subject_id, student_id)",
            "A result already exists for this exam and student/class context.",
        )
    ]

    @api.constrains("result_type", "student_id")
    def _check_result_type(self):
        for record in self:
            if record.result_type == "student" and not record.student_id:
                raise ValidationError("Student is required for student results.")
