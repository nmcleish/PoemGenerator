from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms import validators, ValidationError


class PoemForm(FlaskForm):
    line = TextAreaField("Insert Poem Line", [validators.Required("Please enter a line.")])
    submit = SubmitField("Add Line")
    cancel = SubmitField(label="Cancel", id="cancel")


class FeelForm(FlaskForm):
    feelings = TextAreaField("How are you feeling?", [validators.Required("Please enter your feelings.")])
    generate = SubmitField("Generate Poem")
    replacewords = BooleanField()
