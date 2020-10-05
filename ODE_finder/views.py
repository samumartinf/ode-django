import os

from django.shortcuts import render, redirect
from .tasks import find_structure
from .forms import ExperimentForm, SimulationForm
from .models import Experiment, SimulationResult


def delete_experiment(request, pk):
    if request.method == "POST":
        experiment = Experiment.objects.get(pk=pk)
        experiment.delete()
    return redirect('experiment_list')


def experiment_list(request):
    experiments = Experiment.objects.all()
    results = SimulationResult.objects.all()

    return render(request, 'ODE_finder/experiment_list.html', {
        'experiments': experiments,
        'results': results
    })


def simulation_config(request):
    if request.method == "POST":
        form = SimulationForm(request.POST, request.FILES)
        if form.is_valid():
            experiment = form.cleaned_data['experiment']
            preprocessor = form.cleaned_data['signal_preprocessor']
            title = form.cleaned_data['title']

            find_structure.delay(
                file_path=experiment.csv_file.url,
                experiment_pk=experiment.pk,
                title=title,
                preprocessor=preprocessor
            )

            return redirect('experiment_list')
    else:
        form = SimulationForm()

    return render(request, 'ODE_finder/simulation_config.html', {
        'form': form
    })



def upload_experiment(request):
    if request.method == "POST":
        form = ExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            experiment = Experiment.objects.latest('upload_date')
            file_path = experiment.csv_file.url
            print(file_path)
            return redirect('simulation_config')
    else:
        form = ExperimentForm()

    return render(request, 'ODE_finder/upload_experiment.html', {
        'form': form
    })
