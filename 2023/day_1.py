import sys
import string

def first():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
        print(content)
        total = 0
        for l in content:
            l = l.strip()
            digits = [c for c in l if c.isdigit()]
            first_digit = digits[0]
            last_digit = digits[-1]
            int_str = first_digit + last_digit
            total += int(int_str)
            
        return total

digits_str = {
    "one":"1",
    "two":"2",
    "three" :"3",
    "four":"4",
    "five":"5",
    "six":"6",
    "seven":"7",
    "eight":"8",
    "nine":"9"
}

def detect_digit_in_str(s):
    for digit_str in digits_str.keys():
        if digit_str in s:
            return digits_str[digit_str]
    return None

def get_digits(l):
    digits = []
    # current_digit_str = ""
    for i,c in enumerate(l):
        if c in string.digits:
            digits.append(c)
        else:
            for digit_str in digits_str.keys():
                len_digit = len(digit_str)
                if l[i:i+len_digit] == digit_str:
                    digits.append(digits_str[digit_str])
        # sans la regle eighthree -> 83
        # else:
        #     current_digit_str += c
        #     detection_digit = detect_digit_in_str(current_digit_str)
        #     if detection_digit is not None:
        #         digits.append(detection_digit)
        #         current_digit_str = ""
    return digits

def second():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
        total = 0
        for i,l in enumerate(content):
            l = l.strip()
            digits = get_digits(l)
            first_digit = digits[0]
            last_digit = digits[-1]
            int_str = first_digit + last_digit
            print(f"{ i= } : {digits}, {int_str}")
            total += int(int_str)
            
        return total

    
if __name__ == '__main__':
    result = second()
    print(result)
