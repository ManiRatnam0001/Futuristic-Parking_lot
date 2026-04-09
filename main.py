import threading
import logging
import random
import cv2
import easyocr
import os
class Parking_lot:
    _inst=None
    _lock=threading.Lock()
    def __new__(cls):
        '''Building of parking lot is a single one'''
        if cls._inst == None:
            with cls._lock:
                if cls._inst==None:
                    cls._inst=super().__new__(cls)
        return cls._inst
        '''Threading to ensure that building remains the same'''
    def __init__ (self):
        '''A common log file to have record of transport outgoing and coming
                           in parking lot'''
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler('parker.log')
        self.logger.addHandler(self.file_handler)
        self.formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(logging.INFO)

    def _slots_creation_(self):
        '''Let the owner decide the number of slots he/she wants to have'''
        try:
            self.upper_floor_slot= int(input("Enter the slots you want at upper floor:"))
        except Exception as error:
            self.logger.warning("Error occured, please enter only integers")
            self._slots_creation_()
        try:
            self.middle_floor_slot= int(input("Enter the slots you want in the middle floor:"))
        except Exception as error:
            self.logger.warning("Error occured, please enter only integers")
            self._slots_creation_()
        try:
            self.Ground_floor_slots= int(input("Enter the slots you want at the ground floor:"))
        except Exception as error:
            self.logger.warning("Error occured, please enter only integers")
            self._slots_creation_()

    def avlblty(self):
        '''These will define the space parking lot is going to have'''
        self.elite_space=dict()
        self.common_space=dict()
        self.gnrl_space=dict()

    def book(self):
        '''This can be pre-ordered parking spaces for you'''
        print("There are three different parking space,ELITE ,COMMON  and GENERAL.Choose among them..")
        self.booking=input("Enter the space you want:")
        if self.booking=="ELITE":
            self.slot =random.choice(list(self.elite_space.keys()))
            if self.elite_space[self.slot]==0:
               self._lock.acquire()
               print("Booking is successful")
               print("5$ has been charged from your account")
               self.logger.info(self.slot)
               self.logger.info(self.car_number)
               self.elite_space[self.slot]=1
               self.logger.info(self.elite_space)
            else:
                print("choose other slot")
                self.book()
        elif self.booking=="COMMON":
            self.slot =random.choice(list(self.common_space.keys()))
            if self.common_space[self.slot]==0:
                self._lock.acquire()
                print("Booking is successful")
                print("3$ has been charged from your account")
                self.logger.info(self.slot)
                self.logger.info(self.car_number)
                self.common_space[self.slot]=1
                self.logger.info(self.common_space)
            else:
                print("choose other slot")
                self.book()
        elif self.booking=="GENERAL":
            self.slot=random.choice(list(self.gnrl_space.keys()))
            if self.gnrl_space[self.slot]==0:
                self._lock.acquire()
                self.logger.info(self.slot)
                self.logger.info(self.car_number)
                print("Booking is successful")
                print("2$ has been charged from your account")
                print(self.slot,"has been alloted to you")
                self.gnrl_space[self.slot]=1
                self.logger.info(self.gnrl_space)
            else:
                print("choose other slot`")
                self.book()
        else:
            print("Try again with proper letters and spelling")
            self.book()

    def departure(self):
        '''Time to empty slots'''
        if self.slot in self.elite_space:
            self.elite_space[self.slot] = 0
            self._lock.release()
            self.logger.info(self.slot)
            self.logger.info(self.car_number)
            self.logger.info("departed")
            print("good bye,Have good hours ahead.Here are some candies")
        elif self.slot in self.common_space:
            self.common_space[self.slot] =0
            self._lock.release()
            self.logger.info(self.slot)
            self.logger.info(self.car_number)
            self.logger.info("departed")
            print("bye,Have good hours ahead.")
        elif self.slot in self.gnrl_space:
            self.gnrl_space[self.slot]=0
            self._lock.release()
            self.logger.info(self.slot)
            self.logger.info(self.car_number)
            self.logger.info("departed")
            print("bye,Visit again")

    def range_slots(self):
        '''Lets see the cars we can park in the building'''

        for self.area in range(self.upper_floor_slot):
            self.area= "slot"+str(self.area)
            self.elite_space.update([(self.area,0)])
        self.logger.info(self.elite_space)
        for self.arena in range(self.upper_floor_slot,self.upper_floor_slot+self.middle_floor_slot):
            self.arena="slot"+str(self.arena)
            self.common_space.update([(self.arena,0)])
        self.logger.info(self.common_space)
        for self.var in range(self.middle_floor_slot+self.upper_floor_slot,self.upper_floor_slot+self.middle_floor_slot+self.Ground_floor_slots):
            self.var="slot"+str(self.var)
            self.gnrl_space.update([(self.var,0)])
        self.logger.info(self.gnrl_space)
    def number(self):
        if self.book:
            print("Answer in y/n")
            self.tell=input("do you want to give us manually or should we capture it ?:")
            if self.tell=="y":
                self.car_number=input("enter plate number:")
                return self.car_number
            elif self.tell=="n":
                if not os.path.exists("resources_123"):
                    os.makedirs("resources_123")
                    print("....running...")
                    harcascade = r"C:\Users\HP\Desktop\haarcascade_russian_plate_number.xml"
                    cap = cv2.VideoCapture(0)
                    cap.set(3, 640)
                    cap.set(4, 480)
                    min_area = 500
                    count = 0

                    while True:
                        suc, img = cap.read()
                        if not suc:
                                print("camera not working")
                                break
                        plate_cascade = cv2.CascadeClassifier(harcascade)

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        plates = plate_cascade.detectMultiScale(gray, 1.1, 4)
                        for (x, y, w, h) in plates:
                            area = w * h

                        if area > min_area:

                             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                             img_roi = img[y:y + h, x:x + w]
                             cv2.imshow("ROI", img_roi)

                        cv2.imshow("Result", img)

                        key = cv2.waitKey(1) & 0xFF
                        if key == ord("q"):
                            break
                        elif key == ord("s"):
                             cv2.imwrite("Resources123/" + str(count) + ".jpg", img_roi)
                             cv2.putText(img, "plate saved", (150, 265), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                             cv2.imshow("Result", img)
                             cv2.waitKey(500)
                             count += 1

                             reader = easyocr.Reader(['en'])
                             output = reader.readtext(r"C:\Users\HP\PycharmProjects\Singleton_Project\resources\0.jpg")
                        for char, text, prob in output:
                             self.car_number=text
                             print(self.car_number)
                             return self.car_number
            else:
                print("only y/n")
                self.number()
    def main(self):
        self._slots_creation_()
        self.avlblty()
        self.range_slots()
        self.number()
        self.book()
        self.departure()




a=Parking_lot()
a.main()










