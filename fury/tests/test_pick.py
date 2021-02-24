import numpy as np
from fury import actor, window, ui, pick
from fury.testing import assert_greater
import numpy.testing as npt
import itertools


def test_picking_manager():

    xyz = 10 * np.random.rand(100, 3)
    colors = np.random.rand(100, 4)
    radii = np.random.rand(100) + 0.5

    scene = window.Scene()

    sphere_actor = actor.sphere(centers=xyz,
                                colors=colors,
                                radii=radii)

    scene.add(sphere_actor)

    showm = window.ShowManager(scene,
                               size=(900, 768), reset_camera=False,
                               order_transparent=True)

    showm.initialize()

    tb = ui.TextBlock2D(bold=True)

    # use itertools to avoid global variables
    counter = itertools.count()

    pickm = pick.PickingManager()

    record_indices = {'vertex_indices': [],
                      'face_indices': [],
                      'xyz': [],
                      'actor': []}

    def timer_callback(_obj, _event):
        cnt = next(counter)
        tb.message = "Let's count up to 100 and exit :" + str(cnt)
        showm.scene.azimuth(0.05 * cnt)
        # sphere_actor.GetProperty().SetOpacity(cnt/100.)
        if cnt % 10 == 0:
            # pick at position
            info = pickm.pick((900/2, 768/2), scene)
            record_indices['vertex_indices'].append(info['vertex'])
            record_indices['face_indices'].append(info['face'])
            record_indices['xyz'].append(info['xyz'])
            record_indices['actor'].append(info['actor'])

        showm.render()
        if cnt == 15:
            showm.exit()

    scene.add(tb)

    # Run every 200 milliseconds
    showm.add_timer_callback(True, 200, timer_callback)
    showm.start()

    assert_greater(np.sum(np.array(record_indices['vertex_indices'])), 1)
    assert_greater(np.sum(np.array(record_indices['face_indices'])), 1)

    for ac in record_indices['actor']:
        if ac is not None:
            npt.assert_equal(ac is sphere_actor, True)

    assert_greater(np.sum(np.abs(np.diff(np.array(record_indices['xyz']),
                                         axis=0))), 0)




def test_selector_manager():
    import vtk 
    hsel = vtk.vtkHardwareSelector()
    hsel.SetFieldAssociation(vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS)
    hsel.SetRenderer(scene)

    event_pos = showm.iren.GetEventPosition()
    picking_area = 4
    res = hsel.Select()
    hsel.SetArea(event_pos[0]-picking_area, event_pos[1]-picking_area,
                 event_pos[0]+picking_area, event_pos[1]+picking_area)
    res = hsel.Select()

    num_nodes = res.GetNumberOfNodes()
    if (num_nodes < 1):
        selected_node = None
    else:
        sel_node = res.GetNode(0)
        selected_nodes = set(np.floor(vtknp.vtk_to_numpy(
            sel_node.GetSelectionList())/2).astype(int))
        selected_node = list(selected_nodes)[0]

    if(selected_node is not None):
        if(labels is not None):
            selected_actor.text.SetText(labels[selected_node])
        else:
            selected_actor.text.SetText("#%d" % selected_node)
        selected_actor.SetPosition(positions[selected_node])

    else:
        selected_actor.text.SetText("")


    pass


if __name__ == "__main__":

    test_picking_manager()
