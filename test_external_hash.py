from models.external_hash import ExternalHashStructure
import sys

def test_external_hash():
    print("Testing External Hash Structure...")
    
    # User Example: n=100 (so B=10), Key=2538, Base=9
    # 2*9^3 + 5*9^2 + 3*9^1 + 8*9^0 = 1998
    # 1998 % 10 = 8
    
    eh = ExternalHashStructure(num_records=100, key_length=4, hash_func="conversion_base", base=9)
    print(f"Created structure: Blocks={eh.num_blocks}, Records/Block={eh.records_per_block}")
    
    assert eh.num_blocks == 10
    assert eh.records_per_block == 10
    
    # Test Hash Function
    key = 2538
    h = eh._hash(key)
    print(f"Hash of {key} (Base 9) = {h}")
    assert h == 8
    
    # Test Insert
    idx, area, slot = eh.insert(key)
    print(f"Inserted {key} at Block {idx} ({area}), Slot {slot}")
    assert idx == 8
    assert area == "main"
    assert slot == 0
    
    # Test Search
    res = eh.search(key)
    print(f"Search {key}: {res}")
    assert res == (8, "main", 0)
    
    # Test Collision (Fill block 8)
    # We need 9 more keys that hash to 8.
    # Since we can't easily reverse the hash, we can just force insert into the structure for testing logic
    # or find keys. Let's just manually fill the block to test overflow.
    
    print("Filling block 8...")
    for i in range(1, 10):
        eh.main_structure[8][i] = 2000 + i # Dummy values
        
    # Now Block 8 is full. Next insert should go to collision.
    key2 = 9999 # Let's assume this hashes to 8 or we just force it.
    # Actually, let's just mock the hash for a second or find a key.
    # Easier: just manually check if insert logic handles full block.
    
    # We need a key that hashes to 8 and has length 4.
    # 1009 (base 9) -> 1*729 + 9 = 738 -> 738 % 10 = 8.
    key_collision = 1009
    
    try:
        idx, area, slot = eh.insert(key_collision)
        print(f"Inserted {key_collision} at Block {idx} ({area}), Slot {slot}")
        assert idx == 8
        assert area == "collision"
        assert slot == 0
    except Exception as e:
        print(f"Collision insert failed: {e}")
        raise

    # Test Delete
    eh.delete(key)
    res = eh.search(key)
    print(f"Deleted {key}, Search result: {res}")
    assert res is None

    print("All tests passed!")

if __name__ == "__main__":
    test_external_hash()
