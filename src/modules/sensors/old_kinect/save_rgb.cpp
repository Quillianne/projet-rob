#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <opencv2/opencv.hpp>  // Pour utiliser OpenCV pour manipuler et sauvegarder les images

// Pour compiler ce programme, utilisez la commande suivante:
// g++ -std=c++11 -o save_rgb save_rgb.cpp $(pkg-config --cflags --libs opencv4) -I/path/to/libfreenect2/include -L/path/to/libfreenect2/lib -lfreenect2


int main() {
    // Initialiser libfreenect2 et ouvrir l'appareil Kinect
    libfreenect2::Freenect2 freenect2;
    libfreenect2::Freenect2Device *dev = freenect2.openDevice(freenect2.getDefaultDeviceSerialNumber());

    if (dev == nullptr) {
        std::cerr << "Erreur lors de l'ouverture du périphérique Kinect!" << std::endl;
        return -1;
    }

    // Démarrer les flux (RGB et profondeur)
    dev->start();

    // Préparer l'écouteur pour les trames
    libfreenect2::SyncMultiFrameListener listener(libfreenect2::Frame::Color);
    dev->setColorFrameListener(&listener);


    // Attendre qu'une nouvelle trame RGB et Depth soit reçue
    libfreenect2::FrameMap frames;
    if (!listener.waitForNewFrame(frames, 10*1000)) { // Timeout de 10 secondes
        return -1;
    }

    // Récupérer la trame RGB (image couleur)
    libfreenect2::Frame *rgb_frame = frames[libfreenect2::Frame::Color];

    // Convertir la trame RGB en une image OpenCV (cv::Mat)
    cv::Mat rgb_mat(rgb_frame->height, rgb_frame->width, CV_8UC4, rgb_frame->data);

    // Sauvegarder les images en PNG
    cv::imwrite("photo.png", rgb_mat);  // Sauvegarde l'image couleur

    // Libérer les ressources
    listener.release(frames);
    dev->stop();
    dev->close();

    return 0;
}

