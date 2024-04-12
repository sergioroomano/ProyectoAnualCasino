// Funcion que controla el comportamiento para mover las fichas
function makeDraggable(element) {
    var startPosition = { left: element.style.left, top: element.style.top };
    var ficha_name = element.id;
    element.style.position = "absolute";

    element.onmousedown = function(event) {
        event.preventDefault();
        var offsetX = event.clientX - element.getBoundingClientRect().left;
        var offsetY = event.clientY - element.getBoundingClientRect().top;

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp, { once: true });

        function onMouseMove(event) {
            element.style.left = (event.pageX - offsetX) + "px";
            element.style.top = (event.pageY - offsetY) + "px";
        }

        // Funcion que controla el comportamiento para soltar las fichas
        function onMouseUp(event) {
            document.removeEventListener('mousemove', onMouseMove);

            // Para seleccionar las dropzones que estan overlapping la ficha
            var overlappingZones = [];
            var dropZones = document.querySelectorAll('.drop-zone[data-accepts="ficha"]');
            dropZones.forEach(function(zone) {
                var rect = zone.getBoundingClientRect();
                var chipRect = element.getBoundingClientRect();

                if (!(chipRect.right < rect.left ||
                      chipRect.left > rect.right ||
                      chipRect.bottom < rect.top ||
                      chipRect.top > rect.bottom)) {
                    overlappingZones.push(zone.id);
                }
            });

            if (overlappingZones.length > 0) {
                spawnNewFicha(element, startPosition);
                notificarDropZone(overlappingZones, ficha_name);
            } else {
                element.style.left = startPosition.left;
                element.style.top = startPosition.top;
            }
        }
    };

    element.ondragstart = function() {
        return false;
    };
}

// Cuando la ficha se suelta en una dropzone
function isDroppedInDropZone(x, y) {
    var dropZones = document.querySelectorAll('.drop-zone[data-accepts="ficha"]');
    return Array.from(dropZones).some(zone => {
        var rect = zone.getBoundingClientRect();
        return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
    });
}

// Crear nueva ficha y hacer que se pueda mover
function spawnNewFicha(originalChip, startPosition) {
    var newChip = originalChip.cloneNode(true);
    originalChip.parentElement.appendChild(newChip);
    newChip.style.left = startPosition.left;
    newChip.style.top = startPosition.top;

    makeDraggable(newChip);
}

//Hacer la llamada AJAX y notificar el backend que se ha soltado en la dropzone
function notificarDropZone(zone, ficha) {
    fetch('/drop-zone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ zone: zone, ficha: ficha}),
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });
}

window.onload = function() {
    document.querySelectorAll('.ficha').forEach(makeDraggable);
};
