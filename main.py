import argparse
import asyncio
import sys

from src.application import Application
from src.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def parse_args():
    """
    Phân tích các tham số dòng lệnh.
    """
    parser = argparse.ArgumentParser(description="Ứng dụng AI XiaoZhi")
    parser.add_argument(
        "--mode",
        choices=["gui", "cli"],
        default="gui",
        help="Chế độ chạy: gui (giao diện đồ họa) hoặc cli (dòng lệnh)",
    )
    parser.add_argument(
        "--protocol",
        choices=["mqtt", "websocket"],
        default="websocket",
        help="Giao thức giao tiếp: mqtt hoặc websocket",
    )
    parser.add_argument(
        "--skip-activation",
        action="store_true",
        help="Bỏ qua quy trình kích hoạt và khởi động ứng dụng ngay (chỉ dùng cho chế độ thử nghiệm)",
    )
    return parser.parse_args()


async def handle_activation(mode: str) -> bool:
    """Xử lý quy trình kích hoạt thiết bị, phụ thuộc vào vòng lặp sự kiện hiện có.

    Args:
        mode: Chế độ chạy, "gui" hoặc "cli"

    Returns:
        bool: Kết quả kích hoạt thành công hay không
    """
    try:
        from src.core.system_initializer import SystemInitializer

        logger.info("Đang kiểm tra quy trình kích hoạt thiết bị...")

        system_initializer = SystemInitializer()
        # Dùng chung xử lý kích hoạt trong SystemInitializer, tự động thích ứng với GUI/CLI
        result = await system_initializer.handle_activation_process(mode=mode)
        success = bool(result.get("is_activated", False))
        logger.info(f"Quy trình kích hoạt hoàn thành, kết quả: {success}")
        return success
    except Exception as e:
        logger.error(f"Quy trình kích hoạt gặp sự cố: {e}", exc_info=True)
        return False


async def start_app(mode: str, protocol: str, skip_activation: bool) -> int:
    """
    Điểm vào chung để khởi động ứng dụng (thực hiện trong vòng lặp sự kiện hiện có).
    """
    logger.info("Khởi động ứng dụng AI XiaoZhi")

    # Xử lý quy trình kích hoạt
    if not skip_activation:
        activation_success = await handle_activation(mode)
        if not activation_success:
            logger.error("Kích hoạt thiết bị thất bại, ứng dụng sẽ thoát")
            return 1
    else:
        logger.warning("Bỏ qua quy trình kích hoạt (chế độ thử nghiệm)")

    # Tạo và khởi động ứng dụng
    app = Application.get_instance()
    return await app.run(mode=mode, protocol=protocol)


if __name__ == "__main__":
    exit_code = 1
    try:
        args = parse_args()
        setup_logging()

        if args.mode == "gui":
            # Trong chế độ GUI, main sẽ tạo QApplication và vòng lặp sự kiện qasync
            try:
                import qasync
                from PyQt5.QtWidgets import QApplication
            except ImportError as e:
                logger.error(f"Chế độ GUI yêu cầu thư viện qasync và PyQt5: {e}")
                sys.exit(1)

            qt_app = QApplication.instance() or QApplication(sys.argv)

            loop = qasync.QEventLoop(qt_app)
            asyncio.set_event_loop(loop)
            logger.info("Đã tạo vòng lặp qasync trong main")

            with loop:
                exit_code = loop.run_until_complete(
                    start_app(args.mode, args.protocol, args.skip_activation)
                )
        else:
            # Chế độ CLI sử dụng vòng lặp sự kiện asyncio chuẩn
            exit_code = asyncio.run(
                start_app(args.mode, args.protocol, args.skip_activation)
            )

    except KeyboardInterrupt:
        logger.info("Ứng dụng bị người dùng ngắt")
        exit_code = 0
    except Exception as e:
        logger.error(f"Ứng dụng thoát vì lỗi: {e}", exc_info=True)
        exit_code = 1
    finally:
        sys.exit(exit_code)
