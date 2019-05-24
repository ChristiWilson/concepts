from django.db import models


class Subject(models.Model):

    VOLUME_I = "VI"
    VOLUME_II = "VII"
    APPENDIX_A = "APA"
    APPENDIX_B = "APB"
    APPENDIX_C = "APC"
    APPENDIX_D = "APD"
    # This might not be needed

    WHERE = [
            (VOLUME_I, "Volume I"),
            (VOLUME_II, "Volume II"),
            (APPENDIX_A, "Appendix A"),
            (APPENDIX_B, "Appendix B"),
            (APPENDIX_C, "Appendix C"),
            (APPENDIX_D, "Appendix D"),
            ]

    INTRODUCTION = "INTRO"
    QUESTION = "QUES"
    ANSWER = "ANS"

    PART_OF = [
            (INTRODUCTION, "Introduction"),
            (QUESTION, "Question"),
            (ANSWER, "Answer"),
            ]

    wherein = models.CharField(
            max_length=3,
            choices=WHERE,
            default=APPENDIX_C,
            help_text="Where in the report",
            )
    partof = models.CharField(
            max_length=5,
            choices=PART_OF,
            default=QUESTION,
            help_text="Is this a question, answer or part of introductory?")
    title = models.CharField(
            max_length=80,
            help_text="What is the subject of the question",
            )
    slug = models.SlugField(
            max_length=80,
            help_text="This is what the url will be"
            )
    pageno = models.PositiveSmallIntegerField(
            help_text="Page of the question, answer or introductory"
            )
    adobepage = models.PositiveSmallIntegerField(
            help_text="What page of the pdf does this reside?",
            null=True,
            blank=True,
            )

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        db_table = "subject"


class Body(models.Model):
    subject = models.ForeignKey(
            Subject,
            on_delete=models.CASCADE,
            verbose_name="subject of",
            help_text="What subject does this text relate to?"
            )
    parent = models.ForeignKey(
            "self",
            on_delete=models.CASCADE,
            verbose_name="subsection of",
            related_name="subsections",
            related_query_name="subsection",
            )
    text = models.TextField(
            max_length=500,
            help_text="Text of the paragraph",
            )
    # set page and adobe page numbers to allow nulls to allow for query testing.
    pageno = models.PositiveSmallIntegerField(
            blank=True,
            null=True,
            )
    adobepage = models.PositiveSmallIntegerField(
            blank=True,
            null=True,
            )

    def __str__(self):
        return "Paragraph of question {}".format(self.subject.title)

    class Meta:
        db_table = "body"
