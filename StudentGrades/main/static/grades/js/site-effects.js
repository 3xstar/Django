(() => {
    const audio = document.getElementById("siteAudio");
    const fileInput = document.getElementById("audioFileInput");
    const selectButton = document.getElementById("audioSelectButton");
    const toggleButton = document.getElementById("audioToggleButton");
    const toggleIcon = document.getElementById("audioToggleIcon");
    const trackName = document.getElementById("audioTrackName");
    const status = document.getElementById("audioStatus");
    const player = document.getElementById("siteAudioPlayer");
    const effects = document.getElementById("musicEffects");

    if (!audio || !fileInput || !selectButton || !toggleButton || !effects) {
        return;
    }

    let activeUrl = null;
    let noteTimer = null;
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    function showNote() {
        if (reducedMotion.matches) {
            return;
        }

        const note = document.createElement("span");
        const notes = ["♪", "♫", "♬", "♩"];
        note.className = "music-note";
        note.textContent = notes[Math.floor(Math.random() * notes.length)];
        note.style.setProperty("--note-x", `${8 + Math.random() * 84}%`);
        note.style.setProperty("--note-drift", `${Math.round(Math.random() * 90 - 45)}px`);
        effects.append(note);
        note.addEventListener("animationend", () => note.remove(), { once: true });
    }

    function setPlaying(playing) {
        document.body.classList.toggle("audio-playing", playing);
        player?.classList.toggle("is-playing", playing);
        toggleIcon.textContent = playing ? "Ⅱ" : "▶";
        toggleButton.setAttribute("aria-label", playing ? "Pause music" : "Play music");

        if (noteTimer) {
            window.clearInterval(noteTimer);
            noteTimer = null;
        }
        if (playing) {
            showNote();
            noteTimer = window.setInterval(showNote, 780);
            status.textContent = "Now playing on this device.";
        }
    }

    selectButton.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", () => {
        const file = fileInput.files?.[0];
        if (!file) {
            return;
        }

        audio.pause();
        if (activeUrl) {
            URL.revokeObjectURL(activeUrl);
        }
        activeUrl = URL.createObjectURL(file);
        audio.src = activeUrl;
        audio.load();
        trackName.textContent = file.name;
        toggleButton.disabled = false;
        status.textContent = "Track ready. Press play when you’re ready.";
    });

    toggleButton.addEventListener("click", async () => {
        if (audio.paused) {
            try {
                await audio.play();
            } catch {
                status.textContent = "Could not play this file. Try another audio track.";
            }
        } else {
            audio.pause();
        }
    });

    audio.addEventListener("play", () => setPlaying(true));
    audio.addEventListener("pause", () => setPlaying(false));
    audio.addEventListener("ended", () => {
        setPlaying(false);
        status.textContent = "Track finished. Press play to listen again.";
    });
    audio.addEventListener("error", () => {
        setPlaying(false);
        status.textContent = "Could not read this file. Try another audio track.";
    });

    window.addEventListener("pagehide", () => {
        if (activeUrl) {
            URL.revokeObjectURL(activeUrl);
        }
    }, { once: true });
})();
