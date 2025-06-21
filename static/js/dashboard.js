function login_func() {
    window.location.href = "/login"
}
function class_admin_func() {
    window.location.href = "/admin/Schedulair_app/time_table/"
}
function exam_admin_func() {
    window.location.href = "/admin/Schedulair_app/examschedule/"
}
function holiday_admin_func() {
    window.location.href = "/admin/Schedulair_app/holiday/"
}

document.addEventListener("DOMContentLoaded", function () {
    const open_modal = document.getElementById("open-modal");
    const modal_cont = document.getElementById("modal-cont");
    const close_modal_btn = document.getElementById("close-modal-btn");

    if (open_modal && modal_cont && close_modal_btn) {
        open_modal.addEventListener('click', () => {
            modal_cont.classList.add('show');
        });

        close_modal_btn.addEventListener('click', () => {
            modal_cont.classList.remove('show');
        });
    }

    const buttons = document.querySelectorAll(".dropdown-btn");
    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            console.log("Clicked on dropdown:", btn);

            const parent = btn.closest(".class");
            const select = parent.querySelector(".dropdown-select");
            if (select) {
                select.style.display = (select.style.display === "none" || select.style.display === "") ? "block" : "none";
            } else {
                console.warn("Dropdown <select> not found inside:", parent);
            }
        });
    });

});


