# -*- coding: utf-8 -*-

from odoo import fields, models


class ContinuousAssessment(models.Model):
    _name = "edu.continuous.assessment"
    _description = "Continuous Assessment"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    max_score = fields.Float(default=100.0)
    weight = fields.Float(
        default=0.0,
        help="Weight for this assessment in percentage (optional).",
    )

    exam_id = fields.Many2one(
        "edu.exam",
        required=True,
        ondelete="cascade",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        related="exam_id.class_id",
        store=True,
        readonly=True,
        index=True,
    )
    subject_id = fields.Many2one(
        "edu.academic.subject",
        string="Subject",
        related="exam_id.subject_id",
        store=True,
        readonly=True,
        index=True,
    )

    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        related="exam_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
