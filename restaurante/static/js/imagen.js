const input = document.getElementById('avatar');
const preview = document.getElementById('preview');

input.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', function () {
            preview.src = reader.result;
        });

        reader.readAsDataURL(file);
    } else {
        // Si el usuario elimina la imagen, vuelve a poner la por defecto
        preview.src = "{% static 'productos/defaultImage.png' %}";
    }
});