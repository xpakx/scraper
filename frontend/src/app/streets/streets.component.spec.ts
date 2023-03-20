import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StreetsComponent } from './streets.component';

describe('StreetsComponent', () => {
  let component: StreetsComponent;
  let fixture: ComponentFixture<StreetsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StreetsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StreetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
