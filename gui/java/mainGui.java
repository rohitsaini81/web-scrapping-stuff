import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;
import org.json.*; // Use org.json library

public class AppMain extends JFrame {

    private JPanel currentScreen;
    private List<Map<String, Object>> apps;

    public AppMain() {
        setTitle("Apps List");
        setSize(700, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // Load apps from API
        apps = fetchApps();

        // Show initial apps list screen
        showAppsScreen();
    }

    // ----------------------------
    // Screen switching
    // ----------------------------
    public void showScreen(JPanel screen) {
        if (currentScreen != null) {
            remove(currentScreen);
        }
        currentScreen = screen;
        add(currentScreen);
        revalidate();
        repaint();
    }

    // ----------------------------
    // Apps List Screen
    // ----------------------------
    public void showAppsScreen() {
        JPanel panel = new AppsListScreen(this, apps);
        showScreen(panel);
    }

    // ----------------------------
    // Preview Screen
    // ----------------------------
    public void showPreviewScreen(Map<String, Object> appData) {
        JPanel panel = new PreviewScreen(this, appData);
        showScreen(panel);
    }

    // ----------------------------
    // Fetch Apps (dummy API)
    // ----------------------------
    private List<Map<String, Object>> fetchApps() {
        List<Map<String, Object>> list = new ArrayList<>();
        try {
            URL url = new URL("http://localhost:5000/api/apps");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();

            int responseCode = conn.getResponseCode();
            if (responseCode != 200) {
                System.out.println("Failed to fetch apps");
                return list;
            }

            Scanner sc = new Scanner(url.openStream());
            StringBuilder inline = new StringBuilder();
            while (sc.hasNext()) {
                inline.append(sc.nextLine());
            }
            sc.close();

            JSONArray arr = new JSONArray(inline.toString());
            for (int i = 0; i < arr.length(); i++) {
                JSONObject obj = arr.getJSONObject(i);
                list.add(obj.toMap());
            }

        } catch (IOException | JSONException e) {
            e.printStackTrace();
        }
        return list;
    }

    // ----------------------------
    // Main
    // ----------------------------
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new AppMain().setVisible(true);
        });
    }
}

// ============================
// Apps List Screen
// ============================
class AppsListScreen extends JPanel {

    private JTable table;
    private AppMain root;

    public AppsListScreen(AppMain root, List<Map<String, Object>> apps) {
        this.root = root;
        setLayout(new BorderLayout());

        JLabel title = new JLabel("Apps List", SwingConstants.CENTER);
        title.setFont(new Font("Arial", Font.BOLD, 18));
        add(title, BorderLayout.NORTH);

        String[] columns = {"App ID", "Name", "Short Description"};
        DefaultTableModel model = new DefaultTableModel(columns, 0);
        table = new JTable(model);

        for (Map<String, Object> app : apps) {
            model.addRow(new Object[]{
                app.get("app_id"),
                app.get("name"),
                app.get("short_description")
            });
        }

        JScrollPane scrollPane = new JScrollPane(table);
        add(scrollPane, BorderLayout.CENTER);

        // Row click listener
        table.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                int row = table.getSelectedRow();
                if (row >= 0) {
                    Map<String, Object> selectedApp = apps.get(row);
                    root.showPreviewScreen(selectedApp);
                }
            }
        });
    }
}

// ============================
// Preview Screen
// ============================

class PreviewScreen extends JPanel {

    private AppMain root;

    public PreviewScreen(AppMain root, Map<String, Object> appData) {
        this.root = root;
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));

        // Title
        JLabel title = new JLabel("App Preview");
        title.setFont(new Font("Arial", Font.BOLD, 18));
        title.setAlignmentX(Component.CENTER_ALIGNMENT);
        add(title);

        add(Box.createVerticalStrut(10));

        // App info
        add(new JLabel("App ID: " + appData.get("app_id")));
        add(new JLabel("Name: " + appData.get("name")));
        add(new JLabel("Description: " + appData.get("short_description")));

        add(Box.createVerticalStrut(10));

        // ------------------------------
        // Images section
        // ------------------------------
        JPanel imagesPanel = new JPanel();
        imagesPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 10, 0));

        for (int i = 0; i < 3; i++) { // Add 3 example images
            ImageIcon icon = new ImageIcon("error.png"); // same directory
            // Optional: resize image
            Image img = icon.getImage().getScaledInstance(150, 150, Image.SCALE_SMOOTH);
            JLabel imgLabel = new JLabel(new ImageIcon(img));
            imagesPanel.add(imgLabel);
        }

        add(imagesPanel);

        add(Box.createVerticalStrut(10));

        // Back button
        JButton backBtn = new JButton("Back");
        backBtn.setAlignmentX(Component.CENTER_ALIGNMENT);
        backBtn.addActionListener(e -> root.showAppsScreen());
        add(backBtn);
    }
}

