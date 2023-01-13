from minerva_analysis import app
from flask import render_template, request, Response, jsonify, abort, send_file
import io
from PIL import Image
from minerva_analysis import data_path, get_config
from minerva_analysis.server.models import data_model
from minerva_analysis.server.analytics import comparison
from pathlib import Path
from time import time
import pandas as pd
import json
import orjson
from flask_sqlalchemy import SQLAlchemy


@app.route('/init_database', methods=['GET'])
def init_database():
    datasource = request.args.get('datasource')
    data_model.init(datasource)
    resp = jsonify(success=True)
    return resp


@app.route('/config')
def serve_config():
    return get_config()


@app.route('/get_nearest_cell', methods=['GET'])
def get_nearest_cell():
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    datasource = request.args.get('datasource')
    resp = data_model.query_for_closest_cell(x, y, datasource)
    return serialize_and_submit_json(resp)


@app.route('/get_channel_cell_ids', methods=['GET'])
def get_channel_cell_ids():
    datasource = request.args.get('datasource')
    filter = json.loads(request.args.get('filter'))
    resp = data_model.get_channel_cells(datasource, filter)
    return serialize_and_submit_json(resp)


@app.route('/get_cell_ids_phenotype', methods=['GET'])
def get_cell_ids_phenotype():
    datasource = request.args.get('datasource')
    resp = data_model.get_cells_phenotype(datasource)
    return serialize_and_submit_json(resp)


# Gets a row based on the index
@app.route('/get_phenotype_column_name', methods=['GET'])
def get_phenotype_column_name():
    datasource = request.args.get('datasource')
    resp = data_model.get_phenotype_column_name(datasource)
    return serialize_and_submit_json(resp)


# Gets a row based on the index
@app.route('/get_phenotype_description', methods=['GET'])
def get_phenotype_description():
    datasource = request.args.get('datasource')
    resp = data_model.get_phenotype_description(datasource)
    return serialize_and_submit_json(resp)


# Gets a row based on the index
@app.route('/get_database_row', methods=['GET'])
def get_database_row():
    datasource = request.args.get('datasource')
    row = int(request.args.get('row'))
    resp = data_model.get_row(row, datasource)
    return serialize_and_submit_json(resp)


@app.route('/get_channel_names', methods=['GET'])
def get_channel_names():
    datasource = request.args.get('datasource')
    shortnames = bool(request.args.get('shortNames'))
    resp = data_model.get_channel_names(datasource, shortnames)
    return serialize_and_submit_json(resp)


@app.route('/get_phenotypes', methods=['GET'])
def get_phenotypes():
    datasource = request.args.get('datasource')
    resp = data_model.get_phenotypes(datasource)
    return serialize_and_submit_json(resp)


@app.route('/get_color_scheme', methods=['GET'])
def get_color_scheme():
    datasource = request.args.get('datasource')
    refresh = request.args.get('refresh') == 'true'
    resp = data_model.get_color_scheme(datasource, refresh)
    return serialize_and_submit_json(resp)


@app.route('/get_neighborhood', methods=['GET'])
def get_neighborhood():
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    max_distance = float(request.args.get('max_distance'))
    datasource = request.args.get('datasource')
    resp = data_model.get_neighborhood(x, y, datasource, r=max_distance)
    return serialize_and_submit_json(resp)


@app.route('/get_neighborhood_for_spat_corr', methods=['GET'])
def get_neighborhood_for_spat_corr():
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    max_distance = float(request.args.get('max_distance'))
    datasource = request.args.get('datasource')
    resp = data_model.get_neighborhood_for_spat_corr(x, y, datasource, r=max_distance)
    return serialize_and_submit_json(resp)


@app.route('/get_k_results_for_spat_corr', methods=['GET'])
def get_k_results_for_spat_corr():
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    max_distance = float(request.args.get('max_distance'))
    channels = request.args.get('channels').split()[0].split(',')
    datasource = request.args.get('datasource')
    resp = data_model.get_k_results_for_spat_corr(x, y, datasource, r=max_distance, channels=channels)
    return serialize_and_submit_json(resp)


@app.route('/get_num_cells_in_circle', methods=['GET'])
def get_num_cells_in_circle():
    datasource = request.args.get('datasource')
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    r = float(request.args.get('radius'))
    resp = data_model.get_number_of_cells_in_circle(x, y, datasource, r=r)
    return serialize_and_submit_json(resp)


@app.route('/get_gated_cell_ids', methods=['GET'])
def get_gated_cell_ids():
    datasource = request.args.get('datasource')
    filter = json.loads(request.args.get('filter'))
    resp = data_model.get_gated_cells(datasource, filter)
    return serialize_and_submit_json(resp)


@app.route('/get_database_description', methods=['GET'])
def get_database_description():
    datasource = request.args.get('datasource')
    resp = data_model.get_datasource_description(datasource)
    return serialize_and_submit_json(resp)


@app.route('/upload_gates', methods=['POST'])
def upload_gates():
    file = request.files['file']
    if file.filename.endswith('.csv') == False:
        abort(422)
    datasource = request.form['datasource']
    save_path = data_path / datasource
    if save_path.is_dir() == False:
        abort(422)

    filename = 'uploaded_gates.csv'
    file.save(Path(save_path / filename))
    resp = jsonify(success=True)
    return resp


@app.route('/get_rect_cells', methods=['GET'])
def get_rect_cells():
    # Parse (rect - [x, y, r], channels [string])
    datasource = request.args.get('datasource')
    rect = [float(x) for x in request.args.get('rect').split(',')]
    channels = request.args.get('channels')

    # Retrieve cells - FIXME: Too slow - jam is stalling image loading
    resp = data_model.get_rect_cells(datasource, rect, channels)
    print('Neighborhood size:', len(resp))
    return serialize_and_submit_json(resp)


@app.route('/get_ome_metadata', methods=['GET'])
def get_ome_metadata():
    datasource = request.args.get('datasource')
    resp = data_model.get_ome_metadata(datasource).json()
    # OME-Types handles jsonify itself, so skip the orjson conversion
    response = app.response_class(
        response=resp,
        mimetype='application/json'
    )
    return response


@app.route('/download_gating_csv', methods=['POST'])
def download_gating_csv():
    datasource = request.form['datasource']
    filter = json.loads(request.form['filter'])
    channels = json.loads(request.form['channels'])
    fullCsv = json.loads(request.form['fullCsv'])
    if fullCsv:
        csv = data_model.download_gating_csv(datasource, filter, channels)
    else:
        csv = data_model.download_gates(datasource, filter, channels)
    return Response(
        csv.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=gating_csv.csv"})


@app.route('/get_uploaded_gating_csv_values', methods=['GET'])
def get_gating_csv_values():
    datasource = request.args.get('datasource')
    file_path = data_path / datasource / 'uploaded_gates.csv'
    if file_path.is_file() == False:
        abort(422)
    csv = pd.read_csv(file_path)
    obj = csv.to_dict(orient='records')
    return serialize_and_submit_json(obj)


# @app.route('/get_histogram_comparison', methods=['GET'])
# def get_histogram_comparison():
#     x = float(request.args.get('point_x'))
#     y = float(request.args.get('point_y'))
#     max_distance = float(request.args.get('max_distance'))
#     datasource = request.args.get('datasource')
#     channels = []
#     if request.args.get('channels') != '':
#         channels = request.args.get('channels').split()[0].split(',')
#     resp = image_similarity.histogramComparison(x, y, datasource, max_distance, channels)
#     return serialize_and_submit_json(resp)

@app.route('/histogram_comparison', methods=['GET'])
def histogram_comparison():
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    max_distance = float(request.args.get('max_distance'))
    datasource = request.args.get('datasource')
    viewport = request.args.getlist('viewport')[0]
    zoomlevel = int(float(request.args.get('zoomlevel')))
    sensitivity = float(request.args.get('sensitivity'))

    # for which channels to compute? (currently only the first)
    channels = []
    if request.args.get('channels') != '':
        channels = request.args.get('channels').split()[0].split(',')

    # call functionality
    resp = comparison.histogramComparison(x, y, datasource, max_distance, channels, viewport, zoomlevel, sensitivity)
    return serialize_and_submit_json(resp)


@app.route('/histogram_comparison_simmap', methods=['GET'])
def histogram_comparison_simmap():
    x = float(request.args.get('point_x'))
    y = float(request.args.get('point_y'))
    max_distance = float(request.args.get('max_distance'))
    datasource = request.args.get('datasource')
    viewport = request.args.getlist('viewport')[0]
    zoomlevel = int(float(request.args.get('zoomlevel')))
    sensitivity = float(request.args.get('sensitivity'))

    # for which channels to compute? (currently only the first)
    channels = []
    if request.args.get('channels') != '':
        channels = request.args.get('channels').split()[0].split(',')

    # call functionality
    resp = comparison.histogramComparisonSimMap(x, y, datasource, max_distance, channels, viewport, zoomlevel,
                                                sensitivity)
    # file_object = io.BytesIO()
    # # write PNG in file-object
    # Image.fromarray(png).save(file_object, 'PNG', compress_level=0)
    # # move to beginning of file so `send_file()` it will read from start
    # file_object.seek(0)
    return serialize_and_submit_json(resp)


@app.route('/save_dot', methods=['POST'])
def save_dot():
    post_data = json.loads(request.data)
    datasource = post_data['datasource']
    dot = post_data['dot']
    resp = data_model.save_dot(datasource, dot)
    return serialize_and_submit_json(resp)


@app.route('/load_dots', methods=['GET'])
def load_dots():
    datasource = request.args.get('datasource')
    dots = data_model.load_dots(datasource)
    dots_dict = [to_dict(dot) for dot in dots]
    return serialize_and_submit_json(dots_dict)


@app.route('/delete_dot', methods=['GET'])
def delete_dot():
    datasource = request.args.get('datasource')
    id = int(request.args.get('id'))
    dots = data_model.delete_dot(datasource, id)
    return serialize_and_submit_json(True)


def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in
            row.__table__.columns}


# E.G /generated/data/melanoma/channel_00_files/13/16_18.png
@app.route('/generated/data/<string:datasource>/<string:channel>/<string:level>/<string:tile>')
def generate_png(datasource, channel, level, tile):
    png = data_model.generate_zarr_png(datasource, channel, level, tile)
    file_object = io.BytesIO()
    # write PNG in file-object
    Image.fromarray(png).save(file_object, 'PNG', compress_level=0)
    # move to beginning of file so `send_file()` it will read from start
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


@app.route('/start_spatial_correlation')
def start_spatial_correlation():
    data_model.spatial_corr([])
    return 'hi'


def serialize_and_submit_json(data):
    response = app.response_class(
        response=orjson.dumps(data, option=orjson.OPT_SERIALIZE_NUMPY),
        mimetype='application/json'
    )
    return response
