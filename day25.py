def find_loopsize(pub_key, sn, mod):
    ls = 0
    val = 1
    found = False
    while not found:
        val = sn * val
        val = val % mod
        found = val == pub_key
        ls += 1
    return ls

def apply_encryption(sn, mod, ls):
    val = 1
    for _ in range(ls):
        val *= sn
        val = val % mod
    return val


if __name__ == "__main__":
    card_pub = 11349501  # puzzle input
    door_pub = 5107328  # puzzle input
    init_sn = 7
    modulo = 20201227

    ls_card = find_loopsize(card_pub, init_sn, modulo)
    encry_key = apply_encryption(door_pub, modulo, ls_card)
    print(f'Part 1: {encry_key}')