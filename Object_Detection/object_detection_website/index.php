<?php
include 'db.php';

// Get selected ecosystem from URL parameter, default to Arduino Ecosystem
$selected_ecosystem = isset($_GET['ecosystem']) ? $_GET['ecosystem'] : 'Arduino';

// Modified query to filter by selected ecosystem
$query = "
    SELECT 
        CASE
            WHEN class_name IN ('Arduino_Uno', 'Arduino ESP32_CAM') THEN 'Arduino'
            WHEN class_name IN ('BreadBoard', 'Adapter') THEN 'ROS'
            WHEN class_name IN ('mouse', 'powerBank') THEN 'Electronic Daily'
        END AS ecosystem,
        class_name,
        detected_count
    FROM (
        SELECT 
            class_name,
            detected_count,
            ROW_NUMBER() OVER (PARTITION BY class_name ORDER BY timestamp DESC) as rn
        FROM detections
        WHERE DATE(timestamp) = CURDATE()
    ) latest
    WHERE rn = 1
    AND CASE
        WHEN class_name IN ('Arduino_Uno', 'Arduino ESP32_CAM') THEN 'Arduino'
        WHEN class_name IN ('BreadBoard', 'Adapter') THEN 'ROS'
        WHEN class_name IN ('mouse', 'powerBank') THEN 'Electronic Daily'
    END = ?
    ORDER BY class_name";

$stmt = $conn->prepare($query);
$stmt->bind_param("s", $selected_ecosystem);
$stmt->execute();
$result = $stmt->get_result();

$records = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $records[] = $row;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Object Detection Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <i class="fas fa-robot"></i>
            <span>Detection System</span>
        </div>
        <nav>
            <a href="?ecosystem=Arduino" class="nav-item <?php echo $selected_ecosystem === 'Arduino' ? 'active' : ''; ?>">
                <i class="fas fa-microchip"></i>
                <span>Arduino Ecosystem</span>
            </a>
            <a href="?ecosystem=ROS" class="nav-item <?php echo $selected_ecosystem === 'ROS' ? 'active' : ''; ?>">
                <i class="fas fa-cogs"></i>
                <span>ROS Ecosystem</span>
            </a>
            <a href="?ecosystem=Electronic Daily" class="nav-item <?php echo $selected_ecosystem === 'Electronic Daily' ? 'active' : ''; ?>">
                <i class="fas fa-laptop"></i>
                <span>Electronic Daily</span>
            </a>
        </nav>
    </div>

    <div class="main-content">
        <header>
            <div class="header-content">
                <h1>Object Detection Dashboard</h1>
                <div class="date-display">
                    <i class="far fa-calendar-alt"></i>
                    <span><?php echo date('l, F j, Y'); ?></span>
                </div>
            </div>
        </header>

        <div class="dashboard-container">
            <div class="ecosystem-info">
                <h2><?php echo htmlspecialchars($selected_ecosystem); ?> Ecosystem</h2>
                <p class="ecosystem-description">
                    <?php
                    switch($selected_ecosystem) {
                        case 'Arduino':
                            echo "Monitoring Arduino Uno and ESP32-CAM devices";
                            break;
                        case 'ROS':
                            echo "Tracking BreadBoard and Adapter components";
                            break;
                        case 'Electronic Daily':
                            echo "Detecting daily electronic devices";
                            break;
                    }
                    ?>
                </p>
            </div>

            <div class="data-cards">
                <?php if (!empty($records)): ?>
                    <?php foreach ($records as $record): ?>
                        <div class="card">
                            <div class="card-icon">
                                <?php
                                $icon = 'microchip';
                                switch($record['class_name']) {
                                    case 'Arduino_Uno':
                                    case 'ESP32_CAM':
                                        $icon = 'microchip';
                                        break;
                                    case 'BreadBoard':
                                    case 'Adapter':
                                        $icon = 'plug';
                                        break;
                                    case 'Mouse':
                                        $icon = 'mouse';
                                        break;
                                    case 'PowerBank':
                                        $icon = 'battery-full';
                                        break;
                                }
                                ?>
                                <i class="fas fa-<?php echo $icon; ?>"></i>
                            </div>
                            <div class="card-content">
                                <h3><?php echo htmlspecialchars($record['class_name']); ?></h3>
                                <div class="detection-count">
                                    <span class="count"><?php echo htmlspecialchars($record['detected_count']); ?></span>
                                    <span class="label">Detections Today</span>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; ?>
                <?php else: ?>
                    <div class="no-data">
                        <i class="fas fa-search"></i>
                        <p>No detections recorded today for this ecosystem.</p>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</body>
</html>
