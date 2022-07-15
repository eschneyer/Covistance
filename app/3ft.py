# install opencv "pip install opencv-python"
import cv2

# distance from camera to object(face) measured
# centimeter
Known_distance = 76.2

# width of face in the real world or Object Plane
# centimeter
Known_width = 14.3

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = ((real_face_width * Focal_Length) / face_width_in_frame)*9
    distance = distance*0.0328084

    # return the distance
    return distance

def calculate_dist(frame, face1, face2):
    (x, y, h, w) = face1
    (x2, y2, h2, w2) = face2

    x += w // 2
    y += h // 2
    x2 += w2 // 2
    y2 += h2 // 2

    pixel_dist = abs((x - x2)) - ((w + w2) / 2)
    avg_width = (w + w2) / 2

    dist = (pixel_dist / avg_width) * 9

    if dist > 12 * 3:
        cv2.line(frame, (x + w // 2, y), (x2 - w2 // 2, y2), GREEN, 32)
    else:
        cv2.line(frame, (x + w // 2, y), (x2 - w2 // 2, y2), RED, 32)

    cv2.putText(
        frame, "Distance: {round(dist / 12, 2)} FT", ((x + (x2 - x) // 2) // 2, (y + y2) // 2),
        fonts, 1, BLACK, 2)

    return dist

def face_data(image):
    face_width = 0  # making face width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height


    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 10)

        # getting face width in the pixels
        face_width = w

    # faces.sort()
    distances = []

    if not type(faces) == tuple:
        faces = faces[faces[:, 0].argsort()]

    for i in range(len(faces) - 1):
        face1 = faces[i]
        face2 = faces[i + 1]

        distances.append(calculate_dist(image, face1, face2))


    # return the face width in pixel
    return face_width


# reading reference_image from directory
'''ref_image = cv2.imread("people.jpeg")
# find the face width(pixels) in the reference_image
ref_image_face_width = face_data(ref_image)
# get the focal by calling "Focal_Length_Finder"
# face width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)
# show the reference image
cv2.imshow("ref_image", ref_image)'''

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture(0)

Focal_length_found = 149.2027972027972

print('Focal length found', Focal_length_found)

# looping through frame, incoming from
# camera/video
while True:

    # reading the frame from camera
    _, frame = cap.read()

    # calling face_data function to find
    # the width of face(pixels) in the frame
    face_width_in_frame = face_data(frame)

    # check if the face is zero then not
    # find the distance
    if face_width_in_frame != 0:
        # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)

        # draw line as background of text
        cv2.line(frame, (30, 30), (370, 30), RED, 32)
        cv2.line(frame, (30, 30), (370, 30), BLACK, 28)

        # Drawing Text on the screen
        cv2.putText(
            frame, f"Distance From Camera: {round(Distance, 2)} FT", (30, 35),
            fonts, 0.6, WHITE, 2)

    # show the frame on the screen
    cv2.imshow("frame", frame)

    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# closing the camera
cap.release()

# closing the the windows that are opened
cv2.destroyAllWindows()
