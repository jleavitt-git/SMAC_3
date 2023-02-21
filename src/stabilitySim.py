'''
Build by depth
Every time a block is placed, check for overhang.
    If overhang (Could be multiple height overhang), ensure strong joints back to a pillar
    If not strong joint, check if block has been hard assigned. If so, fail
        Else take hard assignment from pillar
    

On Completion
    Basic weight checks for soft joints (Only allow 1 blocks overhang soft joints)

See where it goes.
 '''