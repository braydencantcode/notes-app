const input = document.getElementById("note_input");
const add_note_button = document.getElementById("add_note");
const clear_notes_button = document.getElementById("clear_notes");
const log_out_button = document.getElementById("log_out");
const container = document.getElementById("note_container");
const sign_up_button = document.getElementById("sign_up");
const header = document.getElementById("header");
const dark_mode_button = document.getElementById("dark_mode");

function this_creates_note_elements_hai(note) {
    
    const delete_button = document.createElement("button");
    delete_button.className = "delete_button";
    delete_button.setAttribute("data-note_id", note.id);
    delete_button.textContent = "❌";
    container.prepend(delete_button);
    
    const note_text = document.createElement("p");
    note_text.textContent = note.text;
    container.prepend(note_text);

    delete_button.addEventListener("click", async function() {
        const note_id = delete_button.getAttribute("data-note_id");
        await fetch(`/notes/${note_id}`, { method: "DELETE" });
        note_text.remove();
        delete_button.remove();
    });
}

async function load_notes() {
    const response = await fetch("/notes");
    const notes = await response.json();

    notes.forEach(note => {
        this_creates_note_elements_hai(note);
    });
}

async function add_note_button_pressed() {
    const text = input.value.trim();

    if (text != "") {
        const response = await fetch("/notes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        const new_note = await response.json();
        this_creates_note_elements_hai(new_note);

        input.value = "";
        input.setAttribute("placeholder", "Start typing!");
    }
}

async function clear_notes_button_pressed() {
    await fetch("/notes", {
        method: "DELETE"
    });

    container.replaceChildren()
}

async function log_out_button_pressed() {
    await fetch("/logout", {method: "POST"});
    window.location.href = "/login";
}

async function sign_up_button_pressed() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password})
    });

    const result = await response.json();
    if (response.ok) {
        alert("Account successfully created!");
    } else {
        alert(result.error);
    }

}

async function set_username() {
    const response = await fetch("/whoami", {method: "GET",})
    const data = await response.json();
    const username = data.username
    header.textContent = `${username}'s notes`;
}

function dark_mode_button_pressed() {
    document.body.classList.toggle("dark_mode");
}

if (add_note_button) {
    add_note_button.addEventListener("click", add_note_button_pressed)
}
if (clear_notes_button) {
    clear_notes_button.addEventListener("click", clear_notes_button_pressed)
}
if (log_out_button) {
    log_out_button.addEventListener("click", log_out_button_pressed)
}
if (sign_up_button) {
    sign_up_button.addEventListener("click", sign_up_button_pressed)
}
if (dark_mode_button) {
    dark_mode_button.addEventListener("click", dark_mode_button_pressed)
}

if (container) {
    load_notes()
    set_username()
}