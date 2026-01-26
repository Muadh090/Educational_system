# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TeacherAttendance(models.Model):
    _name = "edu.teacher.attendance"
    _description = "Teacher Attendance"
    _order = "attendance_date desc, teacher_id"

    attendance_date = fields.Date(required=True, index=True)
    status = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
            ("late", "Late"),
        ],
        required=True,
        default="present",
        index=True,
    )
    teacher_id = fields.Many2one(
        "edu.teacher",
        required=True,
        ondelete="cascade",
        index=True,
    )
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    note = fields.Text()
    company_id = fields.Many2one(
        "res.company",
        related="teacher_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _sql_constraints = [
        (
            "teacher_attendance_unique",
            "unique(teacher_id, attendance_date)",
            "A teacher can only have one attendance record per date.",
        )
    ]

    @api.constrains("check_in", "check_out")
    def _check_check_in_out(self):
        for record in self:
            if record.check_in and record.check_out and record.check_in > record.check_out:
                raise ValidationError("Check-in must be earlier than check-out.")
