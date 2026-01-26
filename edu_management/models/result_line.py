# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResultLine(models.Model):
    _name = "edu.result.line"
    _description = "Result Line"
    _order = "student_id"

    result_id = fields.Many2one(
        "edu.result",
        required=True,
        ondelete="cascade",
        index=True,
    )
    student_id = fields.Many2one(
        "edu.student",
        required=True,
        ondelete="restrict",
        index=True,
    )
    ca_score = fields.Float(string="CA Score", default=0.0)
    exam_score = fields.Float(string="Exam Score", default=0.0)
    total_score = fields.Float(
        string="Total",
        compute="_compute_total_score",
        store=True,
    )
    grade = fields.Selection(
        [
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
            ("F", "F"),
        ],
        compute="_compute_grade",
        store=True,
    )

    company_id = fields.Many2one(
        "res.company",
        related="result_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _sql_constraints = [
        (
            "result_student_unique",
            "unique(result_id, student_id)",
            "Each student can appear only once per result.",
        )
    ]

    @api.depends("ca_score", "exam_score")
    def _compute_total_score(self):
        for record in self:
            record.total_score = (record.ca_score or 0.0) + (record.exam_score or 0.0)

    @api.depends("total_score")
    def _compute_grade(self):
        for record in self:
            score = record.total_score or 0.0
            if score >= 90:
                record.grade = "A"
            elif score >= 80:
                record.grade = "B"
            elif score >= 70:
                record.grade = "C"
            elif score >= 60:
                record.grade = "D"
            elif score >= 50:
                record.grade = "E"
            else:
                record.grade = "F"

    @api.constrains("ca_score", "exam_score")
    def _check_scores(self):
        for record in self:
            if record.ca_score < 0 or record.exam_score < 0:
                raise ValidationError("Scores must be zero or positive.")
