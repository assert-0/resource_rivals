class Client {
  /**
   * @param {string} apiPrefix
   */
  constructor(apiPrefix = "http://localhost:8000") {
    this.apiPrefix = apiPrefix + "/api/v1";
  }

  /**
   * Create a new game
   * @param {{ mapName?: string, mapPath?: string }} options
   * @returns {Promise<Object>} game object
   */
  async createGame({ mapName = null, mapPath = null } = {}) {
    console.log("Creating game with options:", { mapName, mapPath });
    const response = await fetch(`${this.apiPrefix}/game`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mapName, mapPath })
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error creating game: ${JSON.stringify(error)}`);
    }
    const { game } = await response.json();
    console.log("Game created successfully:", game);
    return game;
  }

  /**
   * Delete a game
   * @param {string} gameId
   * @returns {Promise<void>}
   */
  async deleteGame(gameId) {
    console.log("Deleting game with ID:", gameId);
    const response = await fetch(`${this.apiPrefix}/game/${gameId}`, {
      method: 'DELETE'
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error deleting game: ${JSON.stringify(error)}`);
    }
    console.log("Game deleted successfully");
  }

  /**
   * Get game info
   * @param {string} gameId
   * @returns {Promise<Object>} game object
   */
  async getGameInfo(gameId) {
    console.log("Fetching game info for ID:", gameId);
    const response = await fetch(`${this.apiPrefix}/game/${gameId}`);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error fetching game info: ${JSON.stringify(error)}`);
    }
    const { game } = await response.json();
    console.log("Game info fetched successfully:", game);
    return game;
  }

  /**
   * Start a game
   * @param {string} gameId
   * @returns {Promise<void>}
   */
  async startGame(gameId) {
    console.log("Starting game with ID:", gameId);
    const response = await fetch(`${this.apiPrefix}/game/${gameId}/start`, {
      method: 'POST'
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error starting game: ${JSON.stringify(error)}`);
    }
    console.log("Game started successfully");
  }

  /**
   * Create a team
   * @param {string} gameId
   * @param {string} name
   * @returns {Promise<Object>} team object
   */
  async createTeam(gameId, name) {
    console.log("Creating team for game ID:", gameId, "with name:", name);
    const response = await fetch(`${this.apiPrefix}/game/${gameId}/team`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error creating team: ${JSON.stringify(error)}`);
    }
    const { team } = await response.json();
    console.log("Team created successfully:", team);
    return team;
  }

  /**
   * Get team info
   * @param {string} gameId
   * @param {string} teamId
   * @returns {Promise<Object>} team object
   */
  async getTeamInfo(gameId, teamId) {
    console.log("Fetching team info for game ID:", gameId, "and team ID:", teamId);
    const response = await fetch(`${this.apiPrefix}/game/${gameId}/team/${teamId}`);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error fetching team info: ${JSON.stringify(error)}`);
    }
    const { team } = await response.json();
    console.log("Team info fetched successfully:", team);
    return team;
  }

  /**
   * Get visible map for a team
   * @param {string} gameId
   * @param {string} teamId
   * @returns {Promise<Array>} sectors array
   */
  async getVisibleMap(gameId, teamId) {
    console.log("Fetching visible map for game ID:", gameId, "and team ID:", teamId);
    const response = await fetch(
      `${this.apiPrefix}/game/${gameId}/team/${teamId}/visible-map`
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error fetching visible map: ${JSON.stringify(error)}`);
    }
    const { sectors } = await response.json();
    console.log("Visible map fetched successfully:", sectors);
    return sectors;
  }

  /**
   * End turn for a team
   * @param {string} gameId
   * @param {string} teamId
   * @returns {Promise<void>}
   */
  async endTurn(gameId, teamId) {
    console.log("Ending turn for game ID:", gameId, "and team ID:", teamId);
    const response = await fetch(
      `${this.apiPrefix}/game/${gameId}/team/${teamId}/end-turn`,
      { method: 'POST' }
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error ending turn: ${JSON.stringify(error)}`);
    }
    console.log("Turn ended successfully");
  }

  /**
   * Get reachable sectors for a unit
   * @param {string} gameId
   * @param {string} teamId
   * @param {string} unitId
   * @returns {Promise<Array>} sectors array
   */
  async getReachableSectors(gameId, teamId, unitId) {
    console.log("Fetching reachable sectors for game ID:", gameId, "and team ID:", teamId, "unit ID:", unitId);
    const response = await fetch(
      `${this.apiPrefix}/game/${gameId}/team/${teamId}/unit/${unitId}/move/reachable-sectors`
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error fetching reachable sectors: ${JSON.stringify(error)}`);
    }
    const { sectors } = await response.json();
    console.log("Reachable sectors fetched successfully:", sectors);
    return sectors;
  }

  /**
   * Move a unit
   * @param {string} gameId
   * @param {string} teamId
   * @param {string} unitId
   * @param {{ x: number, y: number }} targetPosition
   * @returns {Promise<Object>} move result
   */
  async moveUnit(gameId, teamId, unitId, targetPosition) {
    console.log("Moving unit for game ID:", gameId, "and team ID:", teamId, "unit ID:", unitId, "to position:", targetPosition);
    const response = await fetch(
      `${this.apiPrefix}/game/${gameId}/team/${teamId}/unit/${unitId}/move`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targetPosition })
      }
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error moving unit: ${JSON.stringify(error)}`);
    }
    console.log("Unit moved successfully");
    return await response.json();
  }

  /**
   * Get available buildings for a unit
   * @param {string} gameId
   * @param {string} teamId
   * @param {string} unitId
   * @returns {Promise<Array>} available buildings
   */
  async getAvailableBuildings(gameId, teamId, unitId) {
    console.log("Fetching available buildings for game ID:", gameId, "and team ID:", teamId, "unit ID:", unitId);
    const response = await fetch(
      `${this.apiPrefix}/game/${gameId}/team/${teamId}/unit/${unitId}/build/available-buildings`
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error fetching available buildings: ${JSON.stringify(error)}`);
    }
    const { availableBuildings } = await response.json();
    console.log("Available buildings fetched successfully:", availableBuildings);
    return availableBuildings;
  }

  /**
   * Build with a unit
   * @param {string} gameId
   * @param {string} teamId
   * @param {string} unitId
   * @param {string} buildingType
   * @param {string} buildingNamespace
   * @returns {Promise<void>}
   */
  async buildUnit(gameId, teamId, unitId, buildingType, buildingNamespace) {
    console.log("Building unit for game ID:", gameId, "and team ID:", teamId, "unit ID:", unitId, "with building type:", buildingType, "and namespace:", buildingNamespace);
    const response = await fetch(
      `${this.apiPrefix}/game/${gameId}/team/${teamId}/unit/${unitId}/build`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ buildingType, buildingNamespace })
      }
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Error building unit: ${JSON.stringify(error)}`);
    }
    console.log("Unit built successfully");
  }
}

export default Client;
