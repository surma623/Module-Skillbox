def caesar_cipher(string, shift, alphabet="abcdefghijklmnopqrstuvwxyz"):
    shift %= len(alphabet)
    coded_alphabet = alphabet[shift:] + alphabet[:shift]
    return ''.join([coded_alphabet[alphabet.find(letter)] if letter in alphabet else letter for letter in string])


def shift_word(word, shift):
    if shift != 0:
        return word[shift % len(word):] + word[:shift % len(word)]
    else:
        return word


message = "vujgvmCfb tj ufscfu ouib z/vhm jdjuFyqm jt fscfuu uibo jdju/jnqm fTjnqm tj scfuuf ibou fy/dpnqm yDpnqmf " \
          "jt cfuufs boui dbufe/dpnqmj uGmb tj fuufsc ouib oftufe/ bstfTq jt uufscf uibo otf/ef uzSfbebcjmj " \
          "vout/dp djbmTqf dbtft (ubsfo djbmtqf hifopv up csfbl ifu t/svmf ipvhiBmu zqsbdujdbmju fbutc uz/qvsj " \
          "Fsspst tipvme wfsof qbtt foumz/tjm omfttV mjdjumzfyq odfe/tjmf Jo fui dfgb pg hvjuz-bncj gvtfsf fui " \
          "ubujpoufnq up ftt/hv Uifsf vmetip fc pof.. boe sbcmzqsfgf zpom pof pvt..pcwj xbz pu pe ju/ Bmuipvhi " \
          "uibu bzx bzn puo cf wjpvtpc bu jstug ttvomf sfzpv( i/Evud xOp tj scfuuf ibou /ofwfs uipvhiBm fsofw jt " \
          "fopgu cfuufs boui iu++sjh x/op gJ ifu nfoubujpojnqmf tj eibs pu mbjo-fyq tju( b bec /jefb Jg fui " \
          "foubujpojnqmfn jt fbtz up bjo-fyqm ju znb cf b hppe jefb/ bnftqbdftO bsf pof ipoljoh sfbuh efbj .. " \
          "fu(tm pe psfn gp tf\"uip"

eng = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*+!\",-.'("

deciphered_message_1_list = caesar_cipher(message, -1, eng).split()

shift = -3
deciphered_message_2_list = list()
for word in deciphered_message_1_list:
    deciphered_message_2_list.append(shift_word(word, shift))
    if "/" in word:
        shift -= 1

print(' '.join(deciphered_message_2_list).replace('/ ', '\n'))