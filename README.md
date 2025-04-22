# 酒店管理系统  (Hotel Management System)

本项目是一个使用 Flask（Python Web 框架）和 MySQL 构建的酒店管理系统，用于数据库管理。 它提供了一个简单的界面来管理房间、客户、预订和服务。

## 项目结构 (Project Structure)

该项目具有以下结构：

-   `app.py`: 主要应用程序文件，包含 Flask 路由和逻辑。
-   `establish.sql`: SQL 脚本，用于创建必要的数据库表。
-   `GenerateSampleData.py`: Python 脚本，用于生成数据库的示例数据。
-   `templates/`: 目录，包含 Web 界面的 HTML 模板。
    -   `index.html`: 主页 (Home Page)。
    -   `rooms.html`: 房间管理页面 (Rooms Management Page)。
    -   `customers.html`: 客户管理页面 (Customers Management Page)。
    -   `reservations.html`: 预订管理页面 (Reservations Management Page)。
    -   `services.html`: 服务管理页面 (Services Management Page)。
-   `hotel.log`: 用于错误日志记录的日志文件。
-   `README.md`: 本文件，提供项目概述。

## 安装说明 (Setup Instructions)

1.  **安装依赖项 (Install Dependencies):**

    ```bash
    pip install Flask Flask-MySQLdb Faker
    ```

2.  **创建数据库 (Create Database):**

    运行 `establish.sql` 脚本以在 MySQL 数据库中创建必要的表。

3.  **配置 (Configuration):**

    修改 `app.py` 中的数据库配置以匹配您的 MySQL 设置。

4.  **运行应用程序 (Run the Application):**

    ```bash
    python app.py
    ```

## 用法 (Usage)

该应用程序提供以下功能：

-   **房间管理 (Rooms Management):** 添加、删除和查看房间。
-   **客户管理 (Customers Management):** 添加、删除和查看客户。
-   **预订管理 (Reservations Management):** 添加、删除和查看预订。
-   **服务管理 (Services Management):** 添加、删除和查看服务。
-   **会员管理 (Members Management):** 添加、删除和查看会员。
-   **交易管理 (Transactions Management):** 添加、删除和查看交易。
-   **搜索 (Search):** 跨所有表搜索。

## 错误日志记录 (Error Logging)

该应用程序将错误记录到 `hotel.log` 文件。

## 示例数据生成 (Sample Data Generation)

`GenerateSampleData.py` 脚本可用于生成示例数据以进行测试。 使用以下命令运行脚本：

```bash
python GenerateSampleData.py
```
