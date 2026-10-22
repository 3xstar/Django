(() => {
    "use strict";

    const games = [
        { id: "snack-maze", title: "Snack Maze", genre: "Maze chase", year: 1980, inspiration: "Maze-chase classics", icon: "🍩", colors: ["#ff4c9a", "#ffb847"], description: "Guide a hungry donut through a maze. Munch every crumb and dodge the grumpy chefs.", controls: "Arrow keys to move. Collect every crumb; avoid the chefs." },
        { id: "stack-attack", title: "Stack Attack", genre: "Puzzle", year: 1980, inspiration: "Falling-block puzzles", icon: "🧱", colors: ["#4dd9ff", "#a56bff"], description: "Drop wonky blocks, complete full rows, and keep the wobbly pile below the ceiling.", controls: "← → move, ↑ rotate, ↓ drop faster, Space hard drop." },
        { id: "clown-kombat", title: "Clown Kombat", genre: "Fighting", year: 1990, inspiration: "One-on-one arcade fighters", icon: "🤡", colors: ["#ff514d", "#ffc84a"], description: "A honk-first showdown. Move, bop the rival clown, and win the world's least serious title.", controls: "← → move, ↑ jump, Space bop. Land hits before your rival does." },
        { id: "space-ducks", title: "Space Ducks", genre: "Shooter", year: 1980, inspiration: "Fixed-screen space shooters", icon: "🦆", colors: ["#55e6a5", "#50a9ff"], description: "Defend the snack-ship from a formation of suspiciously organized space ducks.", controls: "← → steer, Space fire. Clear the flock before it reaches you." },
        { id: "barrel-panic", title: "Barrel Panic", genre: "Platformer", year: 1980, inspiration: "Single-screen platformers", icon: "🛢️", colors: ["#ff8e47", "#ffe45c"], description: "Climb the wonky scaffolding, hop over runaway barrels, and rescue your very tall friend.", controls: "← → run, Space jump. Reach the top platform." },
        { id: "brick-o-matic", title: "Brick-O-Matic", genre: "Breakout", year: 1970, inspiration: "Ball-and-paddle games", icon: "🧊", colors: ["#ff62c6", "#64d8ff"], description: "Bop a ball into a wall of colorful bricks. Keep it in the air and clear the screen.", controls: "← → move the paddle, Space launch the ball." },
        { id: "snake-snack", title: "Snake Snack", genre: "Arcade action", year: 1990, inspiration: "Classic grid-chase games", icon: "🐍", colors: ["#70ed74", "#e3f45d"], description: "A very hungry noodle has found the picnic. Eat fruit, grow longer, and avoid your own tail.", controls: "Arrow keys steer. Don't hit the walls or your tail." },
        { id: "crosswalk-calamity", title: "Crosswalk Calamity", genre: "Action", year: 1980, inspiration: "Traffic-dodging arcade games", icon: "🐸", colors: ["#80e85c", "#ffe15a"], description: "Hop a tiny frog across busy lanes and find a safe lily pad. The cars have places to be.", controls: "Arrow keys hop one tile. Reach the green pads at the top." },
        { id: "turbo-tofu", title: "Turbo Tofu", genre: "Racing", year: 1990, inspiration: "Arcade road racers", icon: "🏎️", colors: ["#ff6452", "#58dcff"], description: "Take a tiny tofu-mobile down a very twisty road. Dodge traffic and stay on the asphalt.", controls: "← → steer, ↑ accelerate, ↓ brake." },
        { id: "asteroid-janitors", title: "Asteroid Janitors", genre: "Shooter", year: 1970, inspiration: "Rotating-spacecraft shooters", icon: "🪨", colors: ["#b181ff", "#66e5ff"], description: "The galaxy is messy. Spin your little ship, blast space rocks, and tidy up the cosmos.", controls: "← → rotate, ↑ thrust, Space fire." }
    ];

    const grid = document.querySelector("#game-grid");
    if (!grid) return;

    const search = document.querySelector("#game-search");
    const genre = document.querySelector("#genre-filter");
    const year = document.querySelector("#year-filter");
    const style = document.querySelector("#style-filter");
    const count = document.querySelector("#library-count");
    const empty = document.querySelector("#empty-state");
    const status = document.querySelector("#game-status");
    const title = document.querySelector("#selected-title");
    const meta = document.querySelector("#selected-meta");
    const hint = document.querySelector("#controls-hint");
    const screen = document.querySelector("#game-screen");
    let activeGame = null;

    [...new Set(games.map((game) => game.genre))].sort().forEach((name) => {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        genre.append(option);
    });

    function render() {
        const query = search.value.trim().toLowerCase();
        const filtered = games.filter((game) =>
            (!query || `${game.title} ${game.genre} ${game.inspiration}`.toLowerCase().includes(query)) &&
            (!genre.value || game.genre === genre.value) &&
            (!year.value || String(game.year).startsWith(year.value))
        );
        grid.replaceChildren();
        filtered.forEach((game) => {
            const card = document.createElement("article");
            card.className = "game-card";
            card.innerHTML = `
                <div class="game-cover" style="--cover-a:${game.colors[0]};--cover-b:${game.colors[1]}">
                    <span class="game-cover__number">CABINET ${String(games.indexOf(game) + 1).padStart(2, "0")}</span>
                    <span class="game-cover__icon" aria-hidden="true">${game.icon}</span>
                    <span class="game-cover__title">${game.title}</span>
                    <span class="game-cover__spark">✦</span>
                </div>
                <div class="game-card__body">
                    <div class="game-card__tags"><span>${game.genre}</span><span>${game.year}s</span></div>
                    <h3>${game.title}</h3>
                    <p>${game.description}</p>
                    <span class="game-card__inspiration">INSPIRED BY: ${game.inspiration}</span>
                    <button class="button button--play" type="button" data-play="${game.id}">PLAY THIS GAME <span>→</span></button>
                </div>`;
            grid.append(card);
        });
        count.textContent = `${filtered.length} ${filtered.length === 1 ? "cabinet" : "cabinets"} on the wall`;
        empty.hidden = filtered.length !== 0;
    }

    function startGame(game) {
        if (activeGame) activeGame.destroy();
        title.innerHTML = `${game.title} <span>is up.</span>`;
        meta.textContent = `${game.genre} · ${game.year}s arcade era · ${game.inspiration}`;
        hint.textContent = game.controls;
        status.textContent = "PLAYER ONE // PLAYING";
        screen.replaceChildren();
        activeGame = window.ArcadeGames.start(game.id, screen, (message) => {
            status.textContent = message;
        });
        document.querySelector("#cabinet").scrollIntoView({ behavior: "smooth", block: "start" });
    }

    search.addEventListener("input", render);
    genre.addEventListener("change", render);
    year.addEventListener("change", render);
    style.addEventListener("change", () => {
        document.body.dataset.style = style.value;
    });
    grid.addEventListener("click", (event) => {
        const button = event.target.closest("[data-play]");
        if (button) startGame(games.find((game) => game.id === button.dataset.play));
    });
    document.querySelectorAll("[data-control]").forEach((button) => {
        const key = button.dataset.control;
        const press = (event) => {
            event.preventDefault();
            window.dispatchEvent(new KeyboardEvent("keydown", { key, bubbles: true }));
        };
        const release = (event) => {
            event.preventDefault();
            window.dispatchEvent(new KeyboardEvent("keyup", { key, bubbles: true }));
        };
        button.addEventListener("pointerdown", press);
        button.addEventListener("pointerup", release);
        button.addEventListener("pointerleave", release);
        button.addEventListener("pointercancel", release);
    });

    render();
    window.ArcadeCatalog = games;
})();
