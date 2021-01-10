from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, TextField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    send_file = FileField('Excel-Upload',
                          validators=[
                              FileRequired(),
                              FileAllowed(['xlsx']),
                          ])


class ToolForm(FlaskForm):
    name = TextField("Neuer Name")
    force = IntegerField(validators=[InputRequired()])
    width = IntegerField(validators=[InputRequired()])
    height = IntegerField(validators=[InputRequired()])
    length = IntegerField(validators=[InputRequired()])
    roughness = IntegerField(validators=[InputRequired()])
    diameter = IntegerField(validators=[InputRequired()])


class TechnologyForm(FlaskForm):
    position = IntegerField("Position")
    name = TextField("Name")
    roughness_a = IntegerField(validators=[InputRequired()])
    roughness_b = IntegerField(validators=[InputRequired()])
    roughness_c = IntegerField(validators=[InputRequired()])
    roughness_d = IntegerField(validators=[InputRequired()])
    shape_tolerance_a = IntegerField(validators=[InputRequired()])
    shape_tolerance_b = IntegerField(validators=[InputRequired()])
    shape_tolerance_c = IntegerField(validators=[InputRequired()])
    shape_tolerance_d = IntegerField(validators=[InputRequired()])
    max_machining_path_x_a = IntegerField(validators=[InputRequired()])
    max_machining_path_x_b = IntegerField(validators=[InputRequired()])
    max_machining_path_x_c = IntegerField(validators=[InputRequired()])
    max_machining_path_x_d = IntegerField(validators=[InputRequired()])
    max_machining_path_y_a = IntegerField(validators=[InputRequired()])
    max_machining_path_y_b = IntegerField(validators=[InputRequired()])
    max_machining_path_y_c = IntegerField(validators=[InputRequired()])
    max_machining_path_y_d = IntegerField(validators=[InputRequired()])
    max_machining_path_z_a = IntegerField(validators=[InputRequired()])
    max_machining_path_z_b = IntegerField(validators=[InputRequired()])
    max_machining_path_z_c = IntegerField(validators=[InputRequired()])
    max_machining_path_z_d = IntegerField(validators=[InputRequired()])
