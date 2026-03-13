from django.contrib import admin
from .models import (
    UserProfile, LectureSession, TranscriptSegment, GlossaryTerm,
    SessionAttendance, SessionSlide, LectureSummary, QuizQuestion, LectureAnalytics,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'university', 'department']
    list_filter = ['role']


@admin.register(LectureSession)
class LectureSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_code', 'session_code', 'status', 'lecturer', 'created_at']
    list_filter = ['status']
    readonly_fields = ['session_code']


@admin.register(TranscriptSegment)
class TranscriptSegmentAdmin(admin.ModelAdmin):
    list_display = ['session', 'text', 'timestamp']


@admin.register(SessionSlide)
class SessionSlideAdmin(admin.ModelAdmin):
    list_display = ['session', 'slide_number', 'uploaded_at']


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'subject_area']
    list_filter = ['subject_area']
    search_fields = ['term', 'definition']


@admin.register(SessionAttendance)
class SessionAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'mode', 'joined_at']


@admin.register(LectureSummary)
class LectureSummaryAdmin(admin.ModelAdmin):
    list_display = ['session', 'generated_at']
    readonly_fields = ['generated_at']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['session', 'question_type', 'order', 'question_text']
    list_filter = ['question_type']


@admin.register(LectureAnalytics)
class LectureAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['session', 'avg_wpm', 'complexity_score', 'complexity_label', 'generated_at']
    readonly_fields = ['generated_at']
