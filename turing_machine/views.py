# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TuringMachine, Execution
from .parser import TuringMachineParser, MTValidationError
from .simulator import TuringMachineSimulator

def machine_list(request):
    """Muestra la lista de máquinas y procesa la carga de nuevos archivos .mt."""
    if request.method == 'POST' and request.FILES.get('mt_file'):
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        mt_file = request.FILES['mt_file']

        try:
            # Validar el archivo antes de guardarlo usando nuestro Parser
            file_content = mt_file.read().decode('utf-8')
            parser = TuringMachineParser(file_content)
            parser.parse() # Si hay error, levantará MTValidationError
            
            TuringMachine.objects.create(
                name=name,
                description=description,
                mt_file=mt_file
            )
            messages.success(request, "Máquina cargada y validada correctamente.")
        except MTValidationError as e:
            messages.error(request, f"Error de validación semántica: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {str(e)}")
            
        return redirect('machine_list')

    machines = TuringMachine.objects.all().order_by('-created_at')
    return render(request, 'turing_machine/machine_list.html', {'machines': machines})


def machine_detail(request, machine_id):
    """Muestra los detalles y permite ingresar una cadena para evaluar."""
    machine = get_object_or_404(TuringMachine, id=machine_id)
    
    # Extraer los datos parseados para mostrarlos en la vista
    machine.mt_file.seek(0)
    parser = TuringMachineParser(machine.mt_file.read().decode('utf-8'))
    tm_data = parser.parse()

    if request.method == 'POST':
        input_string = request.POST.get('input_string', '')
        
        # Ejecutar simulación completa
        simulator = TuringMachineSimulator(tm_data, input_string)
        final_status = simulator.run_full()
        
        # Guardar historial en la sesión para el "Paso a Paso" sin JavaScript
        request.session['simulation_history'] = simulator.history
        request.session['input_string'] = input_string
        
        # Registrar ejecución en la BD
        execution = Execution.objects.create(
            turing_machine=machine,
            input_string=input_string,
            final_tape=simulator.get_tape_content(),
            status=final_status,
            steps_count=simulator.steps_count
        )
        return redirect('simulation_step', execution_id=execution.id)

    return render(request, 'turing_machine/machine_detail.html', {
        'machine': machine,
        'tm_data': tm_data
    })


def simulation_step(request, execution_id):
    """Maneja la visualización paso a paso recargando la página."""
    execution = get_object_or_404(Execution, id=execution_id)
    history = request.session.get('simulation_history', [])
    
    # Obtener el paso actual desde la URL (por defecto 0)
    current_step = int(request.GET.get('step', 0))
    
    if not history or current_step >= len(history):
        current_step = len(history) - 1 if history else 0

    snapshot = history[current_step] if history else None
    
    return render(request, 'turing_machine/simulation.html', {
        'execution': execution,
        'snapshot': snapshot,
        'current_step': current_step,
        'total_steps': len(history) - 1,
        'history': history
    })