(() => {
    const configNode = document.getElementById("session-timeout-config");
    const warningNode = document.getElementById("session-timeout-warning");

    if (!configNode || !warningNode) {
        return;
    }

    const logoutUrl = configNode.dataset.logoutUrl;
    const usesIdleTimeout = configNode.dataset.usesIdleTimeout === "true";
    const idleTimeoutSeconds = Number(configNode.dataset.idleTimeoutSeconds || 0);
    const warningThresholdSeconds = Number(configNode.dataset.warningThresholdSeconds || 0);

    if (!usesIdleTimeout || !logoutUrl || !idleTimeoutSeconds) {
        return;
    }

    const countdownLabel = warningNode.querySelector("[data-countdown]");
    const trackedEvents = [
        "click",
        "mousemove",
        "mousedown",
        "keydown",
        "scroll",
        "touchstart",
    ];

    let lastActivityAt = Date.now();

    const formatTime = (seconds) => {
        const safeSeconds = Math.max(seconds, 0);
        const minutes = Math.floor(safeSeconds / 60)
            .toString()
            .padStart(2, "0");
        const remainingSeconds = Math.floor(safeSeconds % 60)
            .toString()
            .padStart(2, "0");
        return `${minutes}:${remainingSeconds}`;
    };

    const registerActivity = () => {
        lastActivityAt = Date.now();
        warningNode.classList.add("hidden");
    };

    const logoutForTimeout = () => {
        window.location.assign(`${logoutUrl}?timeout=idle`);
    };

    trackedEvents.forEach((eventName) => {
        window.addEventListener(eventName, registerActivity, { passive: true });
    });

    window.setInterval(() => {
        const elapsedSeconds = (Date.now() - lastActivityAt) / 1000;
        const remainingSeconds = Math.ceil(idleTimeoutSeconds - elapsedSeconds);

        if (remainingSeconds <= 0) {
            logoutForTimeout();
            return;
        }

        if (remainingSeconds <= warningThresholdSeconds) {
            warningNode.classList.remove("hidden");
            if (countdownLabel) {
                countdownLabel.textContent = formatTime(remainingSeconds);
            }
            return;
        }

        warningNode.classList.add("hidden");
    }, 1000);
})();