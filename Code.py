import cv2
from tkinter import *
from tkinter import filedialog

def scan_qr_opencv_camera():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox[0])):
                pt1 = tuple(bbox[0][i])
                pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                cv2.line(frame, pt1, pt2, color=(255, 0, 0), thickness=2)

            if data:
                cv2.putText(frame, data, pt1, cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)

        cv2.imshow("Escáner QR - Cámara (Presiona 'q' para salir)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def scan_qr_opencv_image():
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.bmp")])
    if not file_path:
        return

    detector = cv2.QRCodeDetector()
    image = cv2.imread(file_path)

    if image is None:
        print("No se pudo cargar la imagen.")
        return

    data, bbox, _ = detector.detectAndDecode(image)

    if bbox is not None:
        bbox = bbox.astype(int)
        for i in range(len(bbox[0])):
            pt1 = tuple(bbox[0][i])
            pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
            cv2.line(image, pt1, pt2, color=(255, 0, 0), thickness=2)

        if data:
            cv2.putText(image, data, pt1, cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
    else:
        print("No se detectó ningún QR.")

    cv2.imshow("Escáner QR - Imagen", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def iniciar_gui():
    ventana = Tk()
    ventana.title("Escáner de QR")
    ventana.geometry("300x200")
    ventana.resizable(False, False)

    Label(ventana, text="Selecciona una opción:", font=("Arial", 14)).pack(pady=20)

    Button(ventana, text="📷 Escanear con cámara", font=("Arial", 12), command=scan_qr_opencv_camera).pack(pady=10)

    Button(ventana, text="🖼️ Subir imagen", font=("Arial", 12), command=scan_qr_opencv_image).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    iniciar_gui()
