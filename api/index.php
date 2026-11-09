<?php
// riddleverse.com tiny stats API (PHP 8 + SQLite). Deployed to /api/index.php
// GET  /api/?stats=YYYY-MM-DD            -> {riddle:{solved,played,avg_ms,hints_avg,top:[...]}, rebus:..., chain:...}
// POST /api/  {date, game, solved, ms, hints, name?}  -> records one result (one per visitor-id per game per day)
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('Access-Control-Allow-Origin: https://riddleverse.com');
$dir = __DIR__ . '/data';
if (!is_dir($dir)) { @mkdir($dir, 0755, true); @file_put_contents($dir . '/.htaccess', "Require all denied\n"); }
try { $db = new PDO('sqlite:' . $dir . '/stats.sqlite'); } catch (Exception $e) { http_response_code(500); echo json_encode(['error' => 'db']); exit; }
$db->exec('CREATE TABLE IF NOT EXISTS results (day TEXT, game TEXT, vid TEXT, solved INTEGER, ms INTEGER, hints INTEGER, name TEXT, ts INTEGER, PRIMARY KEY(day, game, vid))');
$db->exec('CREATE INDEX IF NOT EXISTS idx_day ON results(day, game)');
$games = ['riddle', 'rebus', 'chain'];
function clean_name($n) { $n = trim(preg_replace('/[^\p{L}\p{N} _.\-]/u', '', (string)$n)); return mb_substr($n, 0, 16); }

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $in = json_decode(file_get_contents('php://input'), true);
    if (!$in || !preg_match('/^\d{4}-\d{2}-\d{2}$/', $in['date'] ?? '') || !in_array($in['game'] ?? '', $games)) { http_response_code(400); echo json_encode(['error' => 'bad']); exit; }
    $today = gmdate('Y-m-d'); $yday = gmdate('Y-m-d', time() - 86400);
    if ($in['date'] !== $today && $in['date'] !== $yday) { echo json_encode(['ok' => false, 'reason' => 'archive']); exit; }
    $vid = substr(preg_replace('/[^a-f0-9]/', '', $in['vid'] ?? ''), 0, 32);
    if (strlen($vid) < 16) { http_response_code(400); echo json_encode(['error' => 'vid']); exit; }
    $solved = !empty($in['solved']) ? 1 : 0; $ms = max(0, min(3600000, (int)($in['ms'] ?? 0))); $hints = max(0, min(5, (int)($in['hints'] ?? 0)));
    $name = clean_name($in['name'] ?? '');
    $st = $db->prepare('INSERT OR IGNORE INTO results VALUES (?,?,?,?,?,?,?,?)');
    $st->execute([$in['date'], $in['game'], $vid, $solved, $ms, $hints, $name, time()]);
    if ($name !== '') { $db->prepare('UPDATE results SET name=? WHERE day=? AND game=? AND vid=?')->execute([$name, $in['date'], $in['game'], $vid]); }
    echo json_encode(['ok' => true]); exit;
}
$day = $_GET['stats'] ?? gmdate('Y-m-d');
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $day)) { http_response_code(400); echo json_encode(['error' => 'bad']); exit; }
$out = [];
foreach ($games as $g) {
    $row = $db->prepare('SELECT COUNT(*) played, SUM(solved) solved, AVG(CASE WHEN solved=1 THEN ms END) avg_ms, AVG(CASE WHEN solved=1 THEN hints END) hints_avg FROM results WHERE day=? AND game=?');
    $row->execute([$day, $g]); $r = $row->fetch(PDO::FETCH_ASSOC);
    $top = $db->prepare('SELECT name, ms, hints FROM results WHERE day=? AND game=? AND solved=1 AND name<>"" ORDER BY hints ASC, ms ASC LIMIT 10');
    $top->execute([$day, $g]);
    $out[$g] = ['played' => (int)$r['played'], 'solved' => (int)$r['solved'], 'avg_ms' => $r['avg_ms'] ? (int)$r['avg_ms'] : null, 'hints_avg' => $r['hints_avg'] !== null ? round((float)$r['hints_avg'], 2) : null, 'top' => $top->fetchAll(PDO::FETCH_ASSOC)];
}
$tot = $db->query('SELECT COUNT(DISTINCT vid) FROM results')->fetchColumn();
$out['players_total'] = (int)$tot;
echo json_encode($out);
