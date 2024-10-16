/**
 * @param {number} init_elo The elo of new players
 * @customfunction
 */
function whenTakenElo(values, init_elo = 1000, k_factor_per_point = 20 / 100) {
  values = values ?? [
    ["date", "personne", "score"],
    [new Date("2024-09-26"), "eugene", 584],
    [new Date("2024-09-26"), "valentin", 720],
    [new Date("2024-09-26"), "olivier", 724],
    [new Date("2024-09-27"), "valentin", 650],
    [new Date("2024-09-27"), "gauthier", 716],
    [new Date("2024-09-27"), "eugene", 750],
  ];
  const elos = {};

  const results_per_date = {};
  const results_per_person = {};
  for (const row of values) {
    const person = row[1];
    if (!person) {
      continue;
    }
    const dateDate = row[0];
    if (!(dateDate instanceof Date)) {
      continue;
    }
    const date = dateDate.valueOf();
    if (!results_per_date[date]) {
      results_per_date[date] = [];
    }
    results_per_date[date].push(row);

    if (!results_per_person[person]) {
      results_per_person[person] = 0;
    }
    results_per_person[person]++;
  }

  const all_persons = Object.keys(results_per_person);
  all_persons.sort();

  const all_dates = Object.keys(results_per_date);
  all_dates.sort();
  all_dates.unshift(all_dates[0] - 1000 * 3600 * 24);

  const date_elos = [];

  for (const date of all_dates) {
    const scores = results_per_date[date] ?? [];
    increments = {};
    for (let i = 0; i < scores.length; i++) {
      for (let j = i + 1; j < scores.length; j++) {
        const a = scores[i][1];
        const b = scores[j][1];
        const expected =
          1 /
          (1 +
            Math.pow(
              10,
              ((elos[b] ?? init_elo) - (elos[a] ?? init_elo)) / 400
            ));
        const score_diff = scores[i][2] - scores[j][2];
        const victoryCounts = Math.abs(score_diff);
        const drawCounts = 1000 - victoryCounts;
        const increment =
          k_factor_per_point *
            victoryCounts *
            ((score_diff > 0 ? 1 : 0) - expected) +
          k_factor_per_point * drawCounts * (0.5 - expected);
        increments[a] = (increments[a] ?? 0) + increment;
        increments[b] = (increments[b] ?? 0) - increment;
      }
    }
    for (const player in increments) {
      elos[player] = (elos[player] ?? init_elo) + increments[player];
    }
    date_elos.push({ date: parseInt(date), elos: { ...elos } });
  }
  // final sort per elo
  all_persons.sort((a, b) => elos[a] - elos[b]);
  const header = ["date"];
  header.push(...all_persons);
  const result = [header];
  for (const r of date_elos) {
    result.push(
      [new Date(r.date)].concat(all_persons.map((p) => r.elos[p] ?? init_elo))
    );
  }
  return result;
}
