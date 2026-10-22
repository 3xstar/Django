(() => {
    "use strict";

    const W = 480;
    const H = 320;
    const colors = ["#ffcf54", "#52e8dc", "#ff5c9a", "#b98cff", "#f4f2e8"];
    const rnd = (max) => Math.random() * max;
    const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

    function start(id, host, onStatus) {
        const canvas = document.createElement("canvas");
        canvas.className = "arcade-canvas";
        canvas.width = W;
        canvas.height = H;
        canvas.tabIndex = 0;
        canvas.setAttribute("role", "application");
        canvas.setAttribute("aria-label", `${id.replaceAll("-", " ")} game screen. Use the keyboard or on-screen controls.`);
        host.append(canvas);
        const ctx = canvas.getContext("2d");
        const keys = new Set();
        const state = { score: 0, over: false, won: false, time: 0, last: 0, running: true };
        const keydown = (event) => {
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(event.key)) event.preventDefault();
            keys.add(event.key);
            if (state.over && (event.key === " " || event.key.toLowerCase() === "r")) reset();
        };
        const keyup = (event) => keys.delete(event.key);
        window.addEventListener("keydown", keydown);
        window.addEventListener("keyup", keyup);
        canvas.focus({ preventScroll: true });

        function reset() {
            Object.assign(state, { score: 0, over: false, won: false, time: 0, last: 0 });
            keys.clear();
            initialize();
        }
        function finish(won = false) {
            if (state.over) return;
            state.over = true;
            state.won = won;
            onStatus(won ? `YOU WIN // SCORE ${state.score}` : `GAME OVER // SCORE ${state.score}`);
        }
        function addScore(amount = 10) {
            state.score += amount;
            onStatus(`PLAYER ONE // SCORE ${state.score}`);
        }
        function text(value, x, y, size = 16, color = "#f4f2e8", align = "left") {
            ctx.fillStyle = color;
            ctx.font = `bold ${size}px "Courier New", monospace`;
            ctx.textAlign = align;
            ctx.fillText(value, x, y);
        }
        function box(x, y, w, h, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x, y, w, h);
        }
        function background(label) {
            box(0, 0, W, H, "#101526");
            ctx.strokeStyle = "rgba(84,232,220,.1)";
            ctx.lineWidth = 1;
            for (let x = 0; x < W; x += 24) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
            for (let y = 0; y < H; y += 24) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
            text(label.toUpperCase(), 12, 20, 12, "#52e8dc");
            text(`SCORE ${state.score}`, W - 12, 20, 12, "#ffcf54", "right");
        }
        function circle(x, y, radius, color) {
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();
        }
        function rect(x, y, w, h, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x, y, w, h);
        }
        function endCard(message) {
            if (!state.over) return;
            rect(74, 116, 332, 90, "rgba(7,10,20,.91)");
            ctx.strokeStyle = "#ffcf54";
            ctx.strokeRect(74, 116, 332, 90);
            text(message, W / 2, 151, 20, state.won ? "#52e8dc" : "#ffcf54", "center");
            text(`SCORE ${state.score}  ·  PRESS SPACE TO RETRY`, W / 2, 178, 12, "#f4f2e8", "center");
        }
        let data;

        function initialize() {
            data = {};
            if (id === "snack-maze") {
                data.map = [
                    "###############", "#.............#", "#.###.###.###.#", "#.............#",
                    "#.###.#.#.###.#", "#.....#.#.....#", "###.#.....#.###",
                    "#...#.....#...#", "#.###.#.#.###.#", "#.............#", "###############"
                ].map((row) => row.split(""));
                data.player = { x: 1, y: 1, dir: [0, 0], move: 0 };
                data.ghosts = [{ x: 13, y: 9, color: "#ff5c9a" }, { x: 13, y: 1, color: "#b98cff" }];
            } else if (id === "stack-attack") {
                data.board = Array.from({ length: 20 }, () => Array(10).fill(""));
                data.pieces = ["1111", "011110", "110011", "011110", "1111", "010111", "111010"];
                data.piece = null; data.px = 3; data.py = 0; data.drop = 0;
                newPiece();
            } else if (id === "clown-kombat") {
                data.player = { x: 90, y: 255, vy: 0, hp: 100, cooldown: 0, face: 1 };
                data.enemy = { x: 380, y: 255, vy: 0, hp: 100, cooldown: 0 };
            } else if (id === "space-ducks") {
                data.player = { x: 240 }; data.bullets = []; data.ducks = [];
                for (let row = 0; row < 3; row++) for (let col = 0; col < 8; col++)
                    data.ducks.push({ x: 48 + col * 52, y: 55 + row * 34, alive: true });
                data.direction = 1; data.cooldown = 0;
            } else if (id === "barrel-panic") {
                data.player = { x: 30, y: 262, vy: 0, grounded: true };
                data.barrels = [];
                data.platforms = [290, 230, 170, 110, 58];
                data.spawn = 0;
            } else if (id === "brick-o-matic") {
                data.paddle = 240; data.ball = { x: 240, y: 260, vx: 0, vy: 0, launched: false };
                data.bricks = [];
                for (let row = 0; row < 4; row++) for (let col = 0; col < 10; col++)
                    data.bricks.push({ x: 30 + col * 42, y: 48 + row * 24, alive: true, color: colors[row % colors.length] });
            } else if (id === "snake-snack") {
                data.snake = [{ x: 10, y: 9 }, { x: 9, y: 9 }, { x: 8, y: 9 }];
                data.dir = { x: 1, y: 0 }; data.nextDir = { x: 1, y: 0 }; data.food = { x: 15, y: 7 }; data.move = 0;
            } else if (id === "crosswalk-calamity") {
                data.player = { x: 10, y: 9 }; data.hop = 0; data.lanes = [];
                for (let row = 1; row < 9; row++) data.lanes.push({ y: row, x: rnd(W), speed: (row % 2 ? 1 : -1) * (1 + rnd(1.4)), width: 45 + rnd(28) });
            } else if (id === "turbo-tofu") {
                data.player = 240; data.traffic = []; data.spawn = 0; data.distance = 0;
            } else if (id === "asteroid-janitors") {
                data.ship = { x: 240, y: 160, a: -Math.PI / 2, vx: 0, vy: 0 };
                data.shots = []; data.rocks = Array.from({ length: 7 }, () => rock());
            }
        }
        function newPiece() {
            const raw = data.pieces[Math.floor(rnd(data.pieces.length))];
            data.piece = { cells: raw.split("").map(Number), w: 3, h: 2, color: colors[Math.floor(rnd(colors.length))] };
            if (raw.length === 4) { data.piece.cells = [1, 1, 1, 1, 0, 0]; data.piece.w = 3; }
            data.px = 3; data.py = 0;
            if (collides(data.px, data.py, data.piece.cells, data.piece.w)) finish();
        }
        function collides(px, py, cells = data.piece.cells, width = data.piece.w) {
            for (let i = 0; i < cells.length; i++) if (cells[i]) {
                const x = px + i % width, y = py + Math.floor(i / width);
                if (x < 0 || x >= 10 || y >= 20 || (y >= 0 && data.board[y][x])) return true;
            }
            return false;
        }
        function lockPiece() {
            data.piece.cells.forEach((filled, i) => {
                const x = data.px + i % data.piece.w, y = data.py + Math.floor(i / data.piece.w);
                if (filled && y >= 0) data.board[y][x] = data.piece.color;
            });
            const before = data.board.length;
            data.board = data.board.filter((row) => row.some((cell) => !cell));
            const cleared = before - data.board.length;
            for (let i = 0; i < cleared; i++) data.board.unshift(Array(10).fill(""));
            if (cleared) addScore(cleared * 100);
            newPiece();
        }
        function rock() {
            return { x: rnd(W), y: rnd(H), vx: rnd(2) - 1, vy: rnd(2) - 1, r: 10 + rnd(14) };
        }
        function update(dt) {
            state.time += dt;
            if (state.over) return;
            if (id === "snack-maze") {
                const p = data.player;
                if (keys.has("ArrowLeft")) p.dir = [-1, 0];
                if (keys.has("ArrowRight")) p.dir = [1, 0];
                if (keys.has("ArrowUp")) p.dir = [0, -1];
                if (keys.has("ArrowDown")) p.dir = [0, 1];
                p.move += dt;
                if (p.move > 0.12) {
                    p.move = 0;
                    const nx = p.x + p.dir[0], ny = p.y + p.dir[1];
                    if (data.map[ny]?.[nx] !== "#") { p.x = nx; p.y = ny; }
                    if (data.map[p.y][p.x] === ".") { data.map[p.y][p.x] = " "; addScore(); }
                    data.ghosts.forEach((g) => {
                        if (rnd(1) < 0.55) {
                            const options = [[1, 0], [-1, 0], [0, 1], [0, -1]].filter(([dx, dy]) => data.map[g.y + dy]?.[g.x + dx] !== "#");
                            if (options.length) { const [dx, dy] = options[Math.floor(rnd(options.length))]; g.x += dx; g.y += dy; }
                        }
                        if (g.x === p.x && g.y === p.y) finish();
                    });
                    if (!data.map.some((row) => row.includes("."))) finish(true);
                }
            } else if (id === "stack-attack") {
                if (keys.has("ArrowLeft") && !keys.has("left-held")) { keys.add("left-held"); if (!collides(data.px - 1, data.py)) data.px--; }
                if (!keys.has("ArrowLeft")) keys.delete("left-held");
                if (keys.has("ArrowRight") && !keys.has("right-held")) { keys.add("right-held"); if (!collides(data.px + 1, data.py)) data.px++; }
                if (!keys.has("ArrowRight")) keys.delete("right-held");
                if (keys.has("ArrowUp") && !keys.has("up-held")) {
                    keys.add("up-held");
                    const rotated = Array.from({ length: data.piece.w * data.piece.h }, (_, i) => data.piece.cells[(data.piece.h - 1 - (i % data.piece.h)) * data.piece.w + Math.floor(i / data.piece.h)] || 0);
                    if (!collides(data.px, data.py, rotated, data.piece.h)) { data.piece.cells = rotated; [data.piece.w, data.piece.h] = [data.piece.h, data.piece.w]; }
                }
                if (!keys.has("ArrowUp")) keys.delete("up-held");
                data.drop += dt * (keys.has("ArrowDown") ? 8 : 1);
                if (keys.has(" ") && !keys.has("space-held")) {
                    keys.add("space-held");
                    while (!collides(data.px, data.py + 1)) data.py++;
                    lockPiece();
                }
                if (!keys.has(" ")) keys.delete("space-held");
                if (data.drop > 0.55) { data.drop = 0; if (collides(data.px, data.py + 1)) lockPiece(); else data.py++; }
            } else if (id === "clown-kombat") {
                const p = data.player, e = data.enemy;
                if (keys.has("ArrowLeft")) { p.x -= 3; p.face = -1; }
                if (keys.has("ArrowRight")) { p.x += 3; p.face = 1; }
                if (keys.has("ArrowUp") && p.y >= 255) p.vy = -9;
                p.vy += 0.45; p.y = Math.min(255, p.y + p.vy); if (p.y === 255) p.vy = 0;
                p.x = clamp(p.x, 20, 450);
                p.cooldown = Math.max(0, p.cooldown - dt);
                e.cooldown = Math.max(0, e.cooldown - dt);
                if (e.x < p.x - 30) e.x += 1.2; else if (e.x > p.x + 30) e.x -= 1.2;
                if (keys.has(" ") && p.cooldown === 0) { p.cooldown = 0.35; if (Math.abs(p.x - e.x) < 72 && Math.abs(p.y - 255) < 45) { e.hp -= 12; addScore(25); } }
                if (Math.abs(p.x - e.x) < 48 && e.cooldown === 0) { e.cooldown = 0.8; p.hp -= 8; if (p.hp <= 0) finish(); }
                if (e.hp <= 0) finish(true);
            } else if (id === "space-ducks") {
                data.player.x = clamp(data.player.x + (keys.has("ArrowLeft") ? -4 : 0) + (keys.has("ArrowRight") ? 4 : 0), 18, 462);
                data.cooldown -= dt;
                if (keys.has(" ") && data.cooldown <= 0) { data.bullets.push({ x: data.player.x, y: 270 }); data.cooldown = 0.22; }
                let alive = data.ducks.filter((d) => d.alive);
                if (alive.length && (alive.some((d) => d.x > 455) || alive.some((d) => d.x < 20))) data.direction *= -1;
                alive.forEach((d) => { d.x += data.direction * 35 * dt; d.y += 12 * dt; if (d.y > 277) finish(); });
                data.bullets = data.bullets.filter((b) => b.y > 20);
                data.bullets.forEach((b) => { b.y -= 6; const target = alive.find((d) => Math.abs(d.x - b.x) < 16 && Math.abs(d.y - b.y) < 16); if (target) { target.alive = false; b.y = 0; addScore(10); } });
                if (!data.ducks.some((d) => d.alive)) finish(true);
            } else if (id === "barrel-panic") {
                const p = data.player;
                p.x = clamp(p.x + (keys.has("ArrowLeft") ? -2.8 : 0) + (keys.has("ArrowRight") ? 2.8 : 0), 8, 462);
                if (keys.has(" ") && p.grounded) { p.vy = -8; p.grounded = false; }
                p.vy += 0.35; p.y += p.vy;
                const platform = data.platforms.find((y) => p.y + 28 >= y && p.y + 28 <= y + 8 && p.vy >= 0);
                if (platform) { p.y = platform - 28; p.vy = 0; p.grounded = true; } else p.grounded = false;
                data.spawn += dt;
                if (data.spawn > 1.8) { data.barrels.push({ x: 475, y: 74, vx: -1.6 }); data.spawn = 0; }
                data.barrels.forEach((b) => { b.x += b.vx; if (Math.abs(b.x - p.x) < 20 && Math.abs(b.y - p.y) < 24) finish(); });
                data.barrels = data.barrels.filter((b) => b.x > -20);
                if (p.y < 48) finish(true);
                if (p.y > H) finish();
                if (p.x > 460) addScore(0);
            } else if (id === "brick-o-matic") {
                const d = data;
                d.paddle = clamp(d.paddle + (keys.has("ArrowLeft") ? -5 : 0) + (keys.has("ArrowRight") ? 5 : 0), 35, 445);
                if (keys.has(" ") && !d.ball.launched) { d.ball.launched = true; d.ball.vx = 2.5; d.ball.vy = -3.5; }
                const b = d.ball;
                if (!b.launched) { b.x = d.paddle; b.y = 269; }
                else {
                    b.x += b.vx; b.y += b.vy;
                    if (b.x < 5 || b.x > 475) b.vx *= -1;
                    if (b.y < 27) b.vy *= -1;
                    if (b.y > 272 && b.y < 286 && Math.abs(b.x - d.paddle) < 48) { b.vy = -Math.abs(b.vy); b.vx += (b.x - d.paddle) * 0.025; }
                    if (b.y > H) finish();
                    const brick = d.bricks.find((item) => item.alive && b.x > item.x && b.x < item.x + 37 && b.y > item.y && b.y < item.y + 17);
                    if (brick) { brick.alive = false; b.vy *= -1; addScore(10); }
                }
                if (!d.bricks.some((item) => item.alive)) finish(true);
            } else if (id === "snake-snack") {
                const d = data;
                if (keys.has("ArrowLeft") && d.dir.x !== 1) d.nextDir = { x: -1, y: 0 };
                if (keys.has("ArrowRight") && d.dir.x !== -1) d.nextDir = { x: 1, y: 0 };
                if (keys.has("ArrowUp") && d.dir.y !== 1) d.nextDir = { x: 0, y: -1 };
                if (keys.has("ArrowDown") && d.dir.y !== -1) d.nextDir = { x: 0, y: 1 };
                d.move += dt;
                if (d.move > 0.12) {
                    d.move = 0; d.dir = d.nextDir;
                    const head = { x: d.snake[0].x + d.dir.x, y: d.snake[0].y + d.dir.y };
                    if (head.x < 0 || head.x >= 24 || head.y < 1 || head.y >= 16 || d.snake.some((s) => s.x === head.x && s.y === head.y)) finish();
                    else {
                        d.snake.unshift(head);
                        if (head.x === d.food.x && head.y === d.food.y) { addScore(10); d.food = { x: Math.floor(rnd(24)), y: 1 + Math.floor(rnd(15)) }; }
                        else d.snake.pop();
                    }
                }
            } else if (id === "crosswalk-calamity") {
                const d = data;
                d.hop -= dt;
                if (d.hop <= 0) {
                    let dx = 0, dy = 0;
                    if (keys.has("ArrowLeft")) dx = -1; else if (keys.has("ArrowRight")) dx = 1;
                    else if (keys.has("ArrowUp")) dy = -1; else if (keys.has("ArrowDown")) dy = 1;
                    if (dx || dy) { d.player.x = clamp(d.player.x + dx, 0, 20); d.player.y = clamp(d.player.y + dy, 0, 9); d.hop = 0.14; }
                }
                d.lanes.forEach((l) => { l.x += l.speed * 85 * dt; if (l.x > W) l.x = -l.width; if (l.x < -l.width) l.x = W; if (Math.floor(l.y) === d.player.y && Math.abs(l.x + l.width / 2 - d.player.x * 24 - 12) < l.width / 2 + 10) finish(); });
                if (d.player.y === 0) { addScore(50); d.player = { x: 10, y: 9 }; }
            } else if (id === "turbo-tofu") {
                const d = data;
                d.player = clamp(d.player + (keys.has("ArrowLeft") ? -3 : 0) + (keys.has("ArrowRight") ? 3 : 0), 44, 436);
                const speed = keys.has("ArrowUp") ? 1.4 : keys.has("ArrowDown") ? 0.55 : 1;
                d.distance += dt * speed;
                d.spawn += dt;
                if (d.spawn > 0.75) { d.traffic.push({ x: 55 + rnd(370), y: -25, color: colors[Math.floor(rnd(colors.length))] }); d.spawn = 0; }
                d.traffic.forEach((car) => { car.y += 130 * speed * dt; if (Math.abs(car.x - d.player) < 29 && car.y > 240 && car.y < 300) finish(); if (car.y > 300) { car.y = 500; addScore(5); } });
                d.traffic = d.traffic.filter((car) => car.y < 400);
                if (d.distance > 40) finish(true);
            } else if (id === "asteroid-janitors") {
                const d = data, s = d.ship;
                if (keys.has("ArrowLeft")) s.a -= 3 * dt;
                if (keys.has("ArrowRight")) s.a += 3 * dt;
                if (keys.has("ArrowUp")) { s.vx += Math.cos(s.a) * 0.12; s.vy += Math.sin(s.a) * 0.12; }
                s.x = (s.x + s.vx + W) % W; s.y = (s.y + s.vy + H) % H; s.vx *= 0.99; s.vy *= 0.99;
                d.fire = (d.fire || 0) - dt;
                if (keys.has(" ") && d.fire <= 0) { d.shots.push({ x: s.x, y: s.y, vx: Math.cos(s.a) * 4, vy: Math.sin(s.a) * 4, life: 1 }); d.fire = 0.2; }
                d.shots.forEach((b) => { b.x += b.vx; b.y += b.vy; b.life -= dt; d.rocks.forEach((r) => { if (Math.hypot(r.x - b.x, r.y - b.y) < r.r) { r.dead = true; b.life = 0; addScore(10); } }); });
                d.shots = d.shots.filter((b) => b.life > 0);
                d.rocks.forEach((r) => { r.x = (r.x + r.vx + W) % W; r.y = (r.y + r.vy + H) % H; if (!r.dead && Math.hypot(r.x - s.x, r.y - s.y) < r.r + 8) finish(); });
                d.rocks = d.rocks.filter((r) => !r.dead);
                if (!d.rocks.length) finish(true);
            }
        }

        function draw() {
            background(id.replaceAll("-", " "));
            if (id === "snack-maze") {
                const cell = 26, ox = 45, oy = 27;
                data.map.forEach((row, y) => row.forEach((tile, x) => {
                    if (tile === "#") rect(ox + x * cell, oy + y * cell, cell - 2, cell - 2, "#42418d");
                    else if (tile === ".") circle(ox + x * cell + 12, oy + y * cell + 12, 2.5, "#ffcf54");
                }));
                circle(ox + data.player.x * cell + 12, oy + data.player.y * cell + 12, 9, "#ffcf54");
                data.ghosts.forEach((g) => { circle(ox + g.x * cell + 12, oy + g.y * cell + 12, 9, g.color); text("•", ox + g.x * cell + 12, oy + g.y * cell + 16, 12, "#101526", "center"); });
            } else if (id === "stack-attack") {
                for (let y = 0; y < 20; y++) for (let x = 0; x < 10; x++) {
                    const localX = x - data.px, localY = y - data.py;
                    const pieceCell = localX >= 0 && localX < data.piece.w && localY >= 0 && localY < data.piece.h
                        ? data.piece.cells[localY * data.piece.w + localX]
                        : 0;
                    const fill = data.board[y][x] || (pieceCell ? data.piece.color : "");
                    if (fill) rect(122 + x * 24, 30 + y * 14, 22, 12, fill);
                }
                ctx.strokeStyle = "#52e8dc"; ctx.strokeRect(120, 28, 244, 282);
            } else if (id === "clown-kombat") {
                rect(0, 278, W, 42, "#32284a"); text("PLAYER 1", 18, 43, 11, "#52e8dc");
                rect(18, 50, 190, 12, "#321d35"); rect(18, 50, 190 * data.player.hp / 100, 12, "#52e8dc");
                rect(272, 50, 190, 12, "#321d35"); rect(272, 50, 190 * data.enemy.hp / 100, 12, "#ff5c9a");
                text("RIVAL CLOWN", 462, 43, 11, "#ff5c9a", "right");
                [data.player, data.enemy].forEach((p, i) => {
                    const x = p.x, y = p.y, color = i ? "#ff5c9a" : "#ffcf54";
                    circle(x, y - 24, 15, "#f4f2e8"); circle(x, y - 27, 14, i ? "#b98cff" : "#ff5c9a");
                    circle(x - 5, y - 29, 2, "#101526"); circle(x + 5, y - 29, 2, "#101526");
                    circle(x, y - 22, 4, "#ff514d"); rect(x - 12, y - 9, 24, 26, color);
                    rect(x - 14, y + 14, 10, 14, "#f4f2e8"); rect(x + 4, y + 14, 10, 14, "#f4f2e8");
                });
            } else if (id === "space-ducks") {
                data.ducks.filter((d) => d.alive).forEach((d, i) => { text(i % 2 ? "🦆" : "🐤", d.x, d.y, 22); });
                rect(data.player.x - 12, 276, 24, 20, "#52e8dc"); rect(data.player.x - 4, 266, 8, 12, "#ffcf54");
                data.bullets.forEach((b) => rect(b.x - 2, b.y, 4, 10, "#ffcf54"));
                if (!data.ducks.some((d) => d.alive)) text("FLOCK CLEARED!", W / 2, 170, 18, "#52e8dc", "center");
            } else if (id === "barrel-panic") {
                data.platforms.forEach((y, i) => { rect(i % 2 ? 20 : 0, y, 460, 6, "#ff8e47"); for (let x = i % 2 ? 20 : 0; x < 470; x += 30) rect(x, y + 6, 3, 12, "#97573b"); });
                text("👑", 418, 48, 25); text("🦍", 25, 78, 25);
                data.barrels.forEach((b) => circle(b.x, b.y, 12, "#b96e36"));
                rect(data.player.x - 9, data.player.y, 18, 28, "#52e8dc"); circle(data.player.x, data.player.y - 5, 8, "#ffcf54");
            } else if (id === "brick-o-matic") {
                data.bricks.filter((b) => b.alive).forEach((b) => rect(b.x, b.y, 37, 17, b.color));
                rect(data.paddle - 42, 280, 84, 9, "#52e8dc"); circle(data.ball.x, data.ball.y, 6, "#ffcf54");
                if (!data.ball.launched) text("PRESS SPACE TO LAUNCH", W / 2, 250, 13, "#f4f2e8", "center");
            } else if (id === "snake-snack") {
                data.snake.forEach((s, i) => rect(s.x * 19 + 12, s.y * 18 + 22, 16, 15, i ? "#52e8dc" : "#ffcf54"));
                text("🍎", data.food.x * 19 + 12, data.food.y * 18 + 37, 16);
            } else if (id === "crosswalk-calamity") {
                rect(0, 28, W, 32, "#21523d"); rect(0, 282, W, 30, "#21523d");
                data.lanes.forEach((l) => { rect(l.x, l.y * 28 + 28, l.width, 20, l.y % 2 ? "#ff5c9a" : "#ffcf54"); rect(l.x + 7, l.y * 28 + 31, l.width - 14, 3, "#fff"); });
                text("🐸", data.player.x * 24, data.player.y * 28 + 49, 21);
            } else if (id === "turbo-tofu") {
                const curve = Math.sin(state.time * 1.8) * 32;
                rect(0, 30, W, H - 30, "#203543");
                ctx.fillStyle = "#354b50";
                ctx.beginPath(); ctx.moveTo(125 + curve, 30); ctx.lineTo(355 + curve, 30); ctx.lineTo(470, H); ctx.lineTo(10, H); ctx.closePath(); ctx.fill();
                for (let y = 35; y < H; y += 35) { const x = 238 + curve + (240 - y) * 0.35; rect(x - 2, y, 4, 15, "#ffcf54"); }
                data.traffic.forEach((car) => rect(car.x - 12, car.y, 24, 35, car.color));
                rect(data.player - 14, 259, 28, 40, "#52e8dc"); rect(data.player - 8, 266, 16, 12, "#172638");
                text(`DISTANCE ${Math.min(100, Math.floor(data.distance * 2.5))}%`, 12, 43, 11, "#f4f2e8");
            } else if (id === "asteroid-janitors") {
                data.rocks.forEach((r) => { ctx.strokeStyle = "#b98cff"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(r.x, r.y, r.r, 0, Math.PI * 2); ctx.stroke(); });
                data.shots.forEach((b) => circle(b.x, b.y, 3, "#ffcf54"));
                const s = data.ship;
                ctx.save(); ctx.translate(s.x, s.y); ctx.rotate(s.a); ctx.fillStyle = "#52e8dc"; ctx.beginPath(); ctx.moveTo(13, 0); ctx.lineTo(-10, -8); ctx.lineTo(-6, 0); ctx.lineTo(-10, 8); ctx.closePath(); ctx.fill(); ctx.restore();
            }
            endCard(state.won ? "NICE ONE!" : "OOPS! TRY AGAIN");
        }

        function frame(now) {
            if (!state.running) return;
            const dt = Math.min((now - (state.last || now)) / 1000, 0.04);
            state.last = now;
            update(dt);
            draw();
            requestAnimationFrame(frame);
        }

        initialize();
        onStatus("PLAYER ONE // SCORE 0");
        requestAnimationFrame(frame);
        return {
            destroy() {
                state.running = false;
                window.removeEventListener("keydown", keydown);
                window.removeEventListener("keyup", keyup);
                canvas.remove();
            }
        };
    }

    window.ArcadeGames = { start };
})();
