# MIT License
#
# Copyright (c) 2016-2018 Matthias Rost, Elias Doehne, Tom Koch, Alexander Elvers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import sys

import click
import treewidth_model_experiments

import alib.cli
from alib import run_experiment, util
from . import modelcreator_ecg_decomposition, randomized_rounding_triumvirate, treewidth_model


@click.group()
def cli():
    pass


@cli.command()
@click.argument('scenario_output_file')
@click.argument('parameters', type=click.File('r'))
@click.option('--threads', default=1)
def generate_scenarios(scenario_output_file, parameters, threads):
    alib.cli.f_generate_scenarios(scenario_output_file, parameters, threads)


@cli.command()
@click.argument('parameters', type=click.File('r'))
@click.option('--threads', default=1)
def treewidth_evaluation(parameters, threads):
    f_treewidth_evaluation(parameters, threads)


def f_treewidth_evaluation(parameter_file, threads):
    click.echo('Generate Scenarios for evaluation of the treewidth model')

    util.ExperimentPathHandler.initialize()

    file_basename = os.path.basename(parameter_file.name).split(".")[0].lower()
    log_file = os.path.join(util.ExperimentPathHandler.LOG_DIR, "{}_parent.log".format(file_basename))
    output_file = os.path.join(util.ExperimentPathHandler.OUTPUT_DIR, "{}_results_{{process_index}}.pickle".format(file_basename))
    util.initialize_root_logger(log_file)
    treewidth_model_experiments.run_experiment_from_yaml(parameter_file, output_file, threads)


@cli.command()
@click.argument('experiment_yaml', type=click.File('r'))
@click.argument('min_scenario_index', type=click.INT)
@click.argument('max_scenario_index', type=click.INT)
@click.option('--concurrent', default=1)
def start_experiment(experiment_yaml,
                     min_scenario_index, max_scenario_index,
                     concurrent):
    click.echo('Start Experiment')
    util.ExperimentPathHandler.initialize()
    file_basename = os.path.basename(experiment_yaml.name).split(".")[0].lower()
    log_file = os.path.join(util.ExperimentPathHandler.LOG_DIR, "{}_experiment_execution.log".format(file_basename))
    util.initialize_root_logger(log_file)

    run_experiment.register_algorithm(
        modelcreator_ecg_decomposition.ModelCreatorCactusDecomposition.ALGORITHM_ID,
        modelcreator_ecg_decomposition.ModelCreatorCactusDecomposition
    )

    run_experiment.register_algorithm(
        randomized_rounding_triumvirate.RandomizedRoundingTriumvirate.ALGORITHM_ID,
        randomized_rounding_triumvirate.RandomizedRoundingTriumvirate
    )

    run_experiment.run_experiment(
        experiment_yaml,
        min_scenario_index, max_scenario_index,
        concurrent
    )


if __name__ == '__main__':
    cli()
