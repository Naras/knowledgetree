package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workHasTagHome")
public class WorkHasTagHome extends EntityHome<WorkHasTag> {

	@In(create = true)
	TagworkHome tagworkHome;
	@In(create = true)
	WorkHome workHome;

	public void setWorkHasTagId(WorkHasTagId id) {
		setId(id);
	}

	public WorkHasTagId getWorkHasTagId() {
		return (WorkHasTagId) getId();
	}

	public WorkHasTagHome() {
		setWorkHasTagId(new WorkHasTagId());
	}

	@Override
	public boolean isIdDefined() {
		if (getWorkHasTagId().getTag() == null
				|| "".equals(getWorkHasTagId().getTag()))
			return false;
		if (getWorkHasTagId().getWork() == null
				|| "".equals(getWorkHasTagId().getWork()))
			return false;
		return true;
	}

	@Override
	protected WorkHasTag createInstance() {
		WorkHasTag workHasTag = new WorkHasTag();
		workHasTag.setId(new WorkHasTagId());
		return workHasTag;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Tagwork tagwork = tagworkHome.getDefinedInstance();
		if (tagwork != null) {
			getInstance().setTagwork(tagwork);
		}
		Work work = workHome.getDefinedInstance();
		if (work != null) {
			getInstance().setWork(work);
		}
	}

	public boolean isWired() {
		if (getInstance().getTagwork() == null)
			return false;
		if (getInstance().getWork() == null)
			return false;
		return true;
	}

	public WorkHasTag getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
