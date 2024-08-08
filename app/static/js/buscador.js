document.addEventListener("DOMContentLoaded", function () {
    var marcaSelect = document.querySelector('select[name="marca"]');
    var segmentoSelect = document.querySelector('select[name="segmento"]');
    var reparacionSelect = document.querySelector('select[name="reparacion"]');

    marcaSelect.addEventListener('change', function () {
        var marcaSeleccionada = marcaSelect.value;

        // Realiza una solicitud AJAX para obtener las opciones actualizadas
        fetch(`/opciones_segmento_reparacion/${marcaSeleccionada}`)
            .then(response => response.json())
            .then(data => {
                // Actualiza las opciones de segmento
                segmentoSelect.innerHTML = '';
                data.segmentos.forEach(segmento => {
                    var option = document.createElement('option');
                    option.text = segmento;
                    option.value = segmento;
                    segmentoSelect.add(option);
                });

                // Actualiza las opciones de reparación
                reparacionSelect.innerHTML = '';
                data.reparaciones.forEach(reparacion => {
                    var option = document.createElement('option');
                    option.text = reparacion;
                    option.value = reparacion;
                    reparacionSelect.add(option);
                });
            })
            .catch(error => console.error('Error al obtener opciones:', error));
    });
});