document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("reservation-date");

    if (dateInput) {
        const today = new Date();

        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, "0");
        const day = String(today.getDate()).padStart(2, "0");

        dateInput.min = `${year}-${month}-${day}`;
    }
});
