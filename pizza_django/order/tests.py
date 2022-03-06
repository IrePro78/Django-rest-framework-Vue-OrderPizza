from order import task

def test_task():
    assert task.create_task.run(1)
    assert task.create_task.run(2)
    assert task.create_task.run(3)